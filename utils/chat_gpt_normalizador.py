import openai
import pandas as pd
import googlemaps
import os

class NormalizadorDirecciones:
    def __init__(self, openai_api_key, gmaps_api_key):
        """
        Inicializa la clase con las API Keys de OpenAI y Google Maps.
        """
        self.openai_api_key = openai_api_key
        self.gmaps_api_key = gmaps_api_key

        # Inicializar clientes
        self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        self.gmaps = googlemaps.Client(key=self.gmaps_api_key)

    def normalizar_direccion(self, direccion, comuna):
        """
        Normaliza una dirección utilizando OpenAI.
        """
        if not direccion or not comuna:
            return ""

        prompt = f"""
        Normaliza la siguiente dirección en Chile eliminando información irrelevante como "Casa", "Depto", "Tel", 
        y corrigiendo errores ortográficos o nombres incorrectos, para que la api de google maps pueda geolocalizarla luego:

        Dirección original: {direccion}, {comuna}, Chile

        Devuelve solo la dirección normalizada, sin explicaciones.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error al normalizar dirección: {direccion}. Error: {e}")
            return direccion  # Devolver dirección original en caso de error

    def procesar_archivo(self, ruta_entrada, ruta_salida):
        """
        Carga un archivo Excel, normaliza las direcciones y guarda el resultado.
        """
        try:
            df = pd.read_excel(ruta_entrada)

            # Verificar que las columnas existen
            columnas_requeridas = ["direccion_beneficiario", "beneficiario_comuna"]
            for col in columnas_requeridas:
                if col not in df.columns:
                    print(f"Error: La columna '{col}' no existe en el archivo.")
                    return

            # Aplicar la normalización a todas las direcciones
            df["direccion_normalizada"] = df.apply(
                lambda row: self.normalizar_direccion(row["direccion_beneficiario"], row["beneficiario_comuna"]),
                axis=1
            )

            # Guardar el archivo procesado
            df.to_excel(ruta_salida, index=False)
            print(f"Proceso completado. Archivo guardado como '{ruta_salida}'.")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")

    def procesar_archivo_avanzada(self, ruta_entrada, ruta_salida):
        """
        Carga un archivo Excel, normaliza las direcciones y guarda el resultado.
        """
        try:
            df = pd.read_excel(ruta_entrada)

            # Verificar que las columnas existen
            columnas_requeridas = ["direccion_normalizada"]
            for col in columnas_requeridas:
                if col not in df.columns:
                    print(f"Error: La columna '{col}' no existe en el archivo.")
                    return

            # Aplicar la normalización a todas las direcciones
            df["direccion_normalizada"] = df.apply(
                lambda row: self.normalizar_direccion_avanzada(row["direccion_normalizada"]),
                axis=1
            )

            # Guardar el archivo procesado
            df.to_excel(ruta_salida, index=False)
            print(f"Proceso completado. Archivo guardado como '{ruta_salida}'.")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")

    def normalizar_direccion_avanzada(self, direccion):
        """
        Normaliza una dirección utilizando OpenAI.
        """
        if not direccion:
            return ""

        prompt = f"""
        Normaliza la siguiente dirección en Chile eliminando información irrelevante como "Casa", "Depto", "Tel", 
        y corrigiendo errores ortográficos o nombres incorrectos, el objetivo es que la api de google maps pueda geolocalizarla luego lo mejor posible:

        Dirección original: {direccion}

        Devuelve solo la dirección normalizada, sin explicaciones.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",  
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error al normalizar dirección: {direccion}. Error: {e}")
            return direccion  # Devolver dirección original en caso de error

