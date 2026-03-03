import folium
import os
import pandas as pd
from branca.element import Template, MacroElement

def generar_mapa_lluvia(df):
    """Genera un mapa profesional que visualiza la integración de datos."""
    if not os.path.exists('images'):
        os.makedirs('images')

    # 1. Mapa Base Claro y Limpio (Fácil de imprimir en reportes)
    m = folium.Map(location=[23.6345, -102.5528], zoom_start=5, tiles="cartodbpositron")

    # 2. Coordenadas de los Estados (Asegúrate que coincidan con tus datos)
    coords = {
        'CDMX': [19.4326, -99.1332], 'Jalisco': [20.6595, -103.3494],
        'Nuevo Leon': [25.6866, -100.3161], 'Veracruz': [19.1738, -96.1342],
        'Chihuahua': [28.6330, -106.0691], 'Yucatan': [20.9674, -89.5926],
        'Chiapas': [16.7569, -93.1292], 'Baja California': [30.8406, -115.2838]
    }

    # 3. Procesamiento de los datos reales que integraste
    resumen = df.groupby('estado').agg({
        'lluvia_binaria': 'mean',
        'radiacion': 'mean',
        'nox_rad_ratio': 'mean'
    }).reset_index()

    # 4. Colocación de marcadores con diseño sólido
    for _, row in resumen.iterrows():
        est = row['estado']
        if est in coords:
            # Color basado en radiación (Naranja fuerte para sol, Azul para sombra/nube)
            color_solido = '#E67E22' if row['radiacion'] > 180 else '#2E86C1'
            
            # El tamaño representa la frecuencia de lluvia (Probabilidad)
            # Multiplicamos por 100 para que sea bien visible
            tamano = row['lluvia_binaria'] * 80 + 10

            folium.CircleMarker(
                location=coords[est],
                radius=tamano,
                popup=folium.Popup(f"""
                    <div style='font-family: sans-serif; font-size: 12px; color: #2C3E50;'>
                        <h4 style='margin-bottom:5px;'>{est}</h4>
                        <hr style='margin:5px 0;'>
                        <b>🌧️ Frecuencia Lluvia:</b> {row['lluvia_binaria']:.2%}<br>
                        <b>☀️ Radiación:</b> {row['radiacion']:.1f} W/m²<br>
                        <b>🧪 Ratio Contaminación:</b> {row['nox_rad_ratio']:.4f}
                    </div>
                """, max_width=200),
                color=color_solido,
                weight=2,
                fill=True,
                fill_color=color_solido,
                fill_opacity=0.6
            ).add_to(m)

    # 5. LEYENDA CLÁSICA PROFESIONAL
    legend_html = """
     <div style="position: fixed; bottom: 40px; left: 40px; width: 200px; height: 120px; 
                 background-color: white; border: 2px solid #2C3E50; z-index:9999; font-size:12px;
                 padding: 10px; border-radius: 5px; font-family: sans-serif; box-shadow: 3px 3px 10px rgba(0,0,0,0.1);">
     <b style="font-size: 13px;">Resumen Geográfico</b><br>
     <hr style="margin: 5px 0;">
     <i style="background: #E67E22; width: 10px; height: 10px; display: inline-block; border-radius: 50%;"></i> Alta Radiación Solar<br>
     <i style="background: #2E86C1; width: 10px; height: 10px; display: inline-block; border-radius: 50%;"></i> Baja Radiación (Nubosidad)<br>
     <br>
     <small>* Tamaño = Probabilidad de Lluvia</small>
     </div>
     """
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save("images/mapa_interactivo_final.html")
    print("✅ Mapa profesional generado en images/mapa_interactivo_final.html")