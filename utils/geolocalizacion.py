import math
import requests


def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Diferencias entre las coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Aplicar fórmula haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radio de la Tierra en kilómetros (6371) o en millas (3956)
    r = 6371
    
    # Calcular la distancia
    distance = c * r
    
    return distance

def get_lat_lon(api_key, address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            geometry = data['results'][0]['geometry']['location']
            return geometry['lat'], geometry['lng']
        else:
            print("Error en la respuesta de la API:", data['status'])
    else:
        print("Error en la solicitud:", response.status_code)

    return None, None
    
def buscar_lugares(api_key, latitud, longitud, radius=50):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    location = f"{latitud},{longitud}"
    params = {
        "key": api_key,
        "location": location,  
        "radius": radius,      
    }

    response = requests.get(url, params=params)
    lugares_lista = []  

    if response.status_code == 200:
        resultados = response.json().get('results', [])
        for lugar in resultados:
            lugares_lista.append({
                "Nombre": lugar.get('name'),
                "Dirección": lugar.get('vicinity')
            })
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)
    
    return lugares_lista