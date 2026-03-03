import urllib.request
import os
import time

# Crear carpeta destino
os.makedirs('datos/crudos/radiacion', exist_ok=True)

# 32 estados (latitud, longitud aproximada capital, nombre_archivo)
estaciones = [
    (19.43, -99.13, "CDMX"),
    (25.67, -100.31, "Nuevo_Leon"),
    (20.67, -103.35, "Jalisco"),
    (21.12, -101.68, "Guanajuato"),
    (19.05, -96.15, "Veracruz"),
    (32.65, -115.47, "Baja_California"),
    (24.14, -110.31, "Baja_California_Sur"),
    (25.43, -101.00, "Coahuila"),
    (24.80, -107.39, "Sinaloa"),
    (29.07, -110.96, "Sonora"),
    (28.63, -106.08, "Chihuahua"),
    (22.15, -100.98, "San_Luis_Potosi"),
    (16.75, -93.11, "Chiapas"),
    (17.07, -96.72, "Oaxaca"),
    (20.97, -89.62, "Yucatan"),
    (21.16, -86.85, "Quintana_Roo"),
    (19.84, -90.53, "Campeche"),
    (17.99, -92.93, "Tabasco"),
    (19.24, -103.72, "Colima"),
    (19.70, -101.19, "Michoacan"),
    (19.28, -99.65, "Estado_de_Mexico"),
    (18.92, -99.23, "Morelos"),
    (19.32, -98.23, "Tlaxcala"),
    (19.04, -98.20, "Puebla"),
    (20.10, -98.75, "Hidalgo"),
    (23.74, -99.14, "Tamaulipas"),
    (21.88, -102.29, "Aguascalientes"),
    (23.22, -106.42, "Durango"),
    (22.77, -102.57, "Zacatecas"),
    (21.50, -104.90, "Nayarit"),
    (24.02, -104.67, "Durango_2"),
    (30.84, -116.61, "BC_Ensenada")
]

print("Descargando radiación solar nacional (2011–2021)...\n")

for lat, lon, estado in estaciones:
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters=ALLSKY_SFC_SW_DWN"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start=20110101"
        f"&end=20211231"
        f"&format=CSV"
    )

    ruta = f"datos/crudos/radiacion/radiacion_{estado}.csv"

    try:
        print(f"Descargando {estado}...")
        urllib.request.urlretrieve(url, ruta)
        print(f"  ✔ Guardado en {ruta}")
        time.sleep(1)  # pequeña pausa para no saturar la API
    except Exception as e:
        print(f"  ✖ Error en {estado}: {e}")

print("\nDescarga nacional completada.")