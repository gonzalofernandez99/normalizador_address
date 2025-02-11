import pandas as pd
import re

def normalizar_direccion(direccion):
    """
    Limpia la dirección eliminando palabras irrelevantes y estandarizando nombres de calles.
    """
    if not isinstance(direccion, str):
        return ""

    direccion = direccion.strip().title()  # Convertimos a formato título y eliminamos espacios extra

    # Lista de abreviaciones comunes a eliminar o reemplazar
    abreviaciones = {
        r"\bPje\b": "Pasaje",
        r"\bPJE.\b": "Pasaje",
        r"\bAv\b": "Avenida",
        r"\bCalle\b": "",
        r"\bBlock\b": "",
        r"\bDPTO\b": "",
        r"\bDepartamento\b": "",
        r"\bPoblacion\b": "",
        r"\bPob\b": ""
    }

    # Reemplazar o eliminar abreviaciones
    for abreviacion, reemplazo in abreviaciones.items():
        direccion = re.sub(abreviacion, reemplazo, direccion, flags=re.IGNORECASE)

    # Eliminar espacios múltiples generados tras reemplazos
    direccion = re.sub(r'\s+', ' ', direccion).strip()

    return direccion


def limpiar_direcciones_excel(ruta_excel, columna_direccion, output_path=None):
    """
    Carga un archivo Excel, limpia TODAS las direcciones y guarda el resultado.
    
    Parámetros:
    - ruta_excel: Ruta del archivo Excel a procesar.
    - columna_direccion: Nombre de la columna con las direcciones.
    - output_path: Ruta opcional para guardar el archivo procesado. Si es None, sobrescribe el original.
    """
    df = pd.read_excel(ruta_excel)

    if columna_direccion not in df.columns:
        print(f"Error: La columna '{columna_direccion}' no existe en el archivo.")
        return

    # Limpiar todas las direcciones
    df[columna_direccion] = df[columna_direccion].apply(normalizar_direccion)

    # Guardar el archivo procesado
    output_path = output_path or ruta_excel  # Si no se especifica salida, sobrescribe el original
    df.to_excel(output_path, index=False)
    
    print(f"Archivo guardado en {output_path}")

