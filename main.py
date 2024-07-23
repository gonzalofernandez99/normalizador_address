import pandas as pd
from utils.geolocalizacion import get_lat_lon
from utils.geolocalizacion import buscar_lugares
import os

def get_lat_long_type(row, api_key):
    address = row['nombre_direccion']
    numero_direccion = row['numero_direccion']
    comuna = row['DSC_COMUNA']
    address_completed = f"{address} {numero_direccion}, {comuna}, Chile"
    lat, lon = get_lat_lon(api_key, address_completed)
    if lat is None:
        return None, None, None
    type_match = buscar_lugares(api_key, lat, lon)
    return lat, lon, type_match

if __name__ == '__main__':
    ruta_excel = 'files/muestra_direcciones.xlsx'
    df = pd.read_excel(ruta_excel)
    api_key = os.getenv("google_maps_api_key")

    for index, row in df.iterrows():
        if pd.notna(row['check']) or row['check_validacion'] == 'NOK':
            print(f"Saltando fila {index + 2}")
            continue
        
        lat, lon, type_match = get_lat_long_type(row, api_key)
        
        df.at[index, 'lat'] = lat
        df.at[index, 'lon'] = lon
        
        if type_match is None:
            df.at[index, 'check'] = "REVISAR"
        else:
            df.at[index, 'check'] = "FINALIZADO"
            df.at[index, 'type_match'] = str(type_match) 

    df.to_excel('files/muestra_direcciones_actualizado.xlsx', index=False)