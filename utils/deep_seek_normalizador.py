import pandas as pd
import googlemaps
import requests  # Para hacer solicitudes HTTP a la API de DeepSeek
import os

class NormalizadorDirecciones:
    def __init__(self, deepseek_api_key, gmaps_api_key):
        """
        Inicializa la clase con las API Keys de DeepSeek y Google Maps.
        """
        self.deepseek_api_key = deepseek_api_key
        self.gmaps_api_key = gmaps_api_key

        # Inicializar clientes
        self.gmaps = googlemaps.Client(key=self.gmaps_api_key)

    def normalizar_direccion(self, direccion, comuna):
        """
        Normaliza una dirección utilizando DeepSeek.
        """
        if not direccion or not comuna:
            return ""

        # Crear el prompt para DeepSeek
        prompt = f"""
        Normaliza la siguiente dirección en Chile eliminando información irrelevante como "Casa", "Depto", "Tel", 
        y corrigiendo errores ortográficos o nombres incorrectos:

        Dirección original: {direccion}, {comuna}, Chile

        Devuelve solo la dirección normalizada, sin explicaciones.
        """

        # Configurar la solicitud a la API de DeepSeek
        url = "https://api.deepseek.com/v1/chat/completions"  # URL de ejemplo (revisar la documentación oficial)
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-model",  # Reemplaza con el modelo correcto
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            # Hacer la solicitud a la API de DeepSeek
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            respuesta_json = response.json()

            # Extraer la dirección normalizada de la respuesta
            direccion_normalizada = respuesta_json["choices"][0]["message"]["content"].strip()
            return direccion_normalizada
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

# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza con tus API Keys
    deepseek_api_key = "TU_DEEPSEEK_API_KEY"
    gmaps_api_key = "TU_GMAPS_API_KEY"

    # Rutas de archivos
    ruta_entrada = "direcciones.xlsx"
    ruta_salida = "direcciones_normalizadas.xlsx"

    # Crear instancia y procesar archivo
    normalizador = NormalizadorDirecciones(deepseek_api_key, gmaps_api_key)
    normalizador.procesar_archivo(ruta_entrada, ruta_salida)