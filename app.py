import streamlit as st
import requests
import pandas as pd
# Insertar en la barra lateral un logo o imagen descriptiva
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2991/2991167.png", width=100)
st.sidebar.title("Menú de Navegación")

# --- MANEJO SEGURO DE LA API KEY ---
# Primero intentamos sacar la clave de los Secrets (para tus invitados)
if "NEWS_API_KEY" in st.secrets:
    api_key = st.secrets["NEWS_API_KEY"]
else:
    # Si no hay Secrets (por ejemplo, si corres el código en tu PC), la pide en la barra lateral
    api_key = st.sidebar.text_input("Introduce tu NewsAPI Key:", type="password")

# Configuración de la interfaz
st.set_page_config(page_title="Noticias y Mapa Nicaragua", layout="wide")

st.title("🇳🇮 Noticias y Ubicación de Nicaragua")
st.markdown("""
    **Desarrollado por:** Yimi Josue Guido Aragón  
    *Estudiante de Ingeniería en Sistemas - UNHSJM* Esta aplicación utiliza la API de NewsAPI para filtrar noticias locales y mostrarlas de forma interactiva.
""")



# 2. Lógica principal
if st.sidebar.button("Actualizar Datos"):
    if api_key:
        # --- SECCIÓN DEL MAPA ---
        # Definimos las coordenadas de Nicaragua para el mapa [cite: 18]
        # st.map requiere un DataFrame con columnas lat y lon
        data_mapa = pd.DataFrame({
            'lat': [12.8654],
            'lon': [-85.2072]
        })
        
        st.subheader("📍 Ubicación Geográfica")
        st.map(data_mapa) 

        # --- SECCIÓN DE NOTICIAS ---
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "Nicaragua",
            "language": "es",
            "sortBy": "publishedAt",
            "pageSize": 10
        }
        headers = {"X-Api-Key": api_key} # Autenticación por Header [cite: 38-39]

        try:
            respuesta = requests.get(url, params=params, headers=headers)
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                articulos = datos.get("articles", [])
                
                if articulos:
                    df = pd.DataFrame(articulos)
                    st.success(f"Se cargaron {len(df)} noticias de Nicaragua.")
                    
                    # Mostrar las noticias en tarjetas
                    for i, row in df.iterrows():
                        with st.expander(row['title']):
                            st.write(f"**Fuente:** {row['source']['name']}")
                            st.write(row['description'])
                            st.link_button("Ver noticia", row['url'])
                    
                    # --- BOTÓN DE DESCARGA (Filtrado de datos) ---
                    st.divider()
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar datos (CSV)",
                        data=csv,
                        file_name="noticias_nicaragua.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No se encontraron noticias recientes.")
            else:
                st.error(f"Error {respuesta.status_code}: {respuesta.text}") # Manejo de errores [cite: 32-36]

        except Exception as e:
            st.error(f"Error de conexión: {e}")
    else:
        st.sidebar.error("⚠️ Ingresa tu API Key.")
else:
    st.info("Presiona 'Actualizar Datos' para ver el mapa y las noticias.")
