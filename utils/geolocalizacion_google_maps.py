import googlemaps
import pandas as pd
import os
import time

class GeolocalizadorGoogle:
    def __init__(self, gmaps_api_key):
        """
        Inicializa la clase con la API Key de Google Maps.
        """
        self.gmaps = googlemaps.Client(key=gmaps_api_key)

    def obtener_lat_lon(self, direccion_completa, comuna):
        """
        Obtiene la latitud y longitud de una dirección usando Google Maps API.
        Si la dirección original no da resultados, intenta con variantes corregidas.
        """

        if not direccion_completa:
            return None, None, "Error", "Falta dirección"

        try:
            # 🔹 PRIMER INTENTO: Buscar con la dirección completa
            geocode_result = self.gmaps.geocode(direccion_completa)

            if not geocode_result:
                print(f"⚠️ No se encontró: {direccion_completa}, intentando con variante...")

                # 🔹 SEGUNDO INTENTO: Buscar solo con la comuna
                direccion_reducida = f"{comuna}, Chile"
                geocode_result = self.gmaps.geocode(direccion_reducida)

                if not geocode_result:
                    return None, None, "Error", "Dirección no encontrada"
            print(geocode_result)
            # ✅ Google encontró una dirección (puede ser corregida)
            location = geocode_result[0]["geometry"]["location"]
            lat, lon = location["lat"], location["lng"]

            # 📌 Tipo de ubicación (ROOFTOP, RANGE_INTERPOLATED, etc.)
            location_type = geocode_result[0]["geometry"]["location_type"]

            # 📌 Dirección corregida por Google
            formatted_address = geocode_result[0]["formatted_address"]

            # 🔄 INTENTAR DE NUEVO SI GOOGLE MAPS CAMBIÓ EL NOMBRE DE LA CALLE
            if direccion_completa.lower() not in formatted_address.lower():
                print(f"🔄 Dirección corregida por Google: {formatted_address}")
                geocode_result_2 = self.gmaps.geocode(formatted_address)

                if geocode_result_2:
                    location_2 = geocode_result_2[0]["geometry"]["location"]
                    lat, lon = location_2["lat"], location_2["lng"]
                    location_type = geocode_result_2[0]["geometry"]["location_type"]
                    formatted_address = geocode_result_2[0]["formatted_address"]

            return lat, lon, location_type, formatted_address

        except Exception as e:
            print(f"❌ Error obteniendo lat/lon para {direccion_completa}: {e}")
            return None, None, "Error", str(e)

    def procesar_archivo(self, ruta_entrada, ruta_salida):
        """
        Carga un archivo Excel, obtiene lat/lon para cada dirección y guarda el resultado.
        """
        try:
            df = pd.read_excel(ruta_entrada)

            # Verificar que las columnas existen
            columnas_requeridas = ["direccion_beneficiario", "beneficiario_comuna"]
            for col in columnas_requeridas:
                if col not in df.columns:
                    print(f"Error: La columna '{col}' no existe en el archivo.")
                    return

            # Aplicar la geolocalización a todas las direcciones
            df[["lat", "lon", "location_type", "formatted_address"]] = df.apply(
                lambda row: pd.Series(
                    self.obtener_lat_lon(row["direccion_normalizada"], row["beneficiario_comuna"])
                ),
                axis=1
            )

            # Guardar el archivo procesado
            df.to_excel(ruta_salida, index=False)
            print(f"✅ Proceso completado. Archivo guardado como '{ruta_salida}'.")

        except Exception as e:
            print(f"❌ Error al procesar el archivo: {e}")
