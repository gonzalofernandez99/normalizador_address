import pandas as pd
from utils.geolocalizacion import get_lat_lon
import os
from utils.chat_gpt_normalizador import NormalizadorDirecciones
import openai
def get_lat_long_type(row, api_key):
    #address = row['direccion_beneficiario']
    #comuna = row['beneficiario_comuna']
    #address_completed = f"{address}, {comuna}, Chile"
    address_completed = row['direccion_normalizada']
    lat, lon, location_type, data, formatted_address = get_lat_lon(api_key, address_completed)
    return lat, lon, location_type, data, formatted_address

def get_lat_long(ruta_excel,output_path):
    
    df = pd.read_excel(ruta_excel)
    api_key = os.getenv("google_maps_api_key")

    for col in ['lat', 'lon', 'check', 'location_type', 'data', 'formatted_address']:
        if col not in df.columns:
            df[col] = None

    df['lat'] = df['lat'].astype(object)
    df['lon'] = df['lon'].astype(object)
    df['check'] = df['check'].astype(str)
    df['location_type'] = df['location_type'].astype(str)
    df['data'] = df['data'].astype(str)
    df['formatted_address'] = df['formatted_address'].astype(str)

    for index, row in df.iterrows():
        if str(row['check']).strip().upper() in ["OK"]:
            print(f"Saltando fila {index + 2}, check ya tiene valor: {row['check']}")
            continue
        
        print(f"Procesando fila {index + 2}")

        lat, lon, location_type, data, formatted_address = get_lat_long_type(row, api_key)

        df.at[index, 'lat'] = lat
        df.at[index, 'lon'] = lon
        df.at[index, 'check'] = "OK" if lat is not None and lon is not None else "NOK"
        df.at[index, 'location_type'] = str(location_type) if location_type else "UNKNOWN"
        df.at[index, 'data'] = str(data) if data else "NO DATA"
        df.at[index, 'formatted_address'] = str(formatted_address) if formatted_address else "NO ADDRESS"

    
    df.to_excel(output_path, index=False)
    print(f"Archivo guardado en {output_path}")
def normalizar_direciones ():
        # Cargar claves desde variables de entorno
    OPENAI_API_KEY = os.getenv("openai_api_key_bst")
    GMAPS_API_KEY = os.getenv("google_maps_api_key")

    # Crear instancia del normalizador
    normalizador = NormalizadorDirecciones(OPENAI_API_KEY, GMAPS_API_KEY)

    # Rutas de los archivos
    ruta_entrada = "files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx"
    ruta_salida = "files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx"

    # Ejecutar el procesamiento
    normalizador.procesar_archivo(ruta_entrada, ruta_salida)

def normalizar_direciones_avanzada():
        # Cargar claves desde variables de entorno
    OPENAI_API_KEY = os.getenv("openai_api_key_bst")
    GMAPS_API_KEY = os.getenv("google_maps_api_key")

    # Crear instancia del normalizador
    normalizador = NormalizadorDirecciones(OPENAI_API_KEY, GMAPS_API_KEY)

    # Rutas de los archivos
    ruta_entrada = "files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx"
    ruta_salida = "files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx"

    # Ejecutar el procesamiento
    normalizador.procesar_archivo_avanzada(ruta_entrada, ruta_salida)

if __name__ == '__main__':
    #ruta_excel = 'files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx'
    #output_path = 'files/Listados_ok_nok/Listado_beneficiarios_nok.xlsx'
    #get_lat_long(ruta_excel,output_path)
    normalizar_direciones_avanzada()



