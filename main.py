import streamlit as st
from PIL import Image
import os
from utils.pubmed_api import buscar_pubmed
from utils.summarizer import resumir_texto
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuración general de la página
st.set_page_config(
    page_title="Monitor de Evidencia",
    layout="wide",
    page_icon="🔬"
)

# Cargar estilos CSS
estilos_path = "assets/estilos.css"
if os.path.exists(estilos_path):
    with open(estilos_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Mostrar logo si existe
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=160)
else:
    st.sidebar.markdown("### 🔬 Monitor de Evidencia")

# Menú de navegación lateral
menu = st.sidebar.radio("Menú principal", ["Dashboard", "Búsqueda", "Configuración"])

# Verificar si la API Key está configurada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.sidebar.warning("⚠️ API Key de OpenAI no configurada. Algunos resúmenes podrían no estar disponibles.")

# Pantalla principal
if menu == "Dashboard":
    st.title("📊 Monitor Científico de Evidencia")
    st.markdown("Bienvenido al sistema de monitoreo de evidencia científica. Selecciona una opción en el menú para comenzar.")
    st.info("Desde aquí podrás ver métricas clave, alertas y tendencias globales de publicaciones.")

elif menu == "Búsqueda":
    st.title("🔍 Buscar Evidencia en PubMed")
    
    with st.form("form_busqueda"):
        query = st.text_input("🔎 Término de búsqueda", value="semaglutide")
        max_resultados = st.slider("Resultados a mostrar", 5, 50, 10)
        submitted = st.form_submit_button("Buscar")
    
    if submitted and query:
        with st.spinner("Consultando PubMed..."):
            resultados = buscar_pubmed(query, max_resultados)
        
        if resultados:
            st.success(f"🔍 {len(resultados)} resultados encontrados para '{query}'")
            
            for r in resultados:
                with st.expander(r["Título"]):
                    st.markdown(f"**PMID:** {r['PMID']}")
                    st.markdown(f"**Autores:** {r['Autores']}")
                    st.markdown(f"**Fuente:** {r['Fuente']}")
                    st.markdown(f"**Resumen original:**\n\n{r['Resumen']}")
                    
                    if api_key:  # Solo intentar resumir si hay API Key
                        st.markdown("**🧠 Resumen generado por IA:**")
                        with st.spinner("Generando resumen con IA..."):
                            resumen_ia = resumir_texto(r["Resumen"])
                            st.info(resumen_ia)
                    else:
                        st.warning("La función de resumen con IA requiere una API Key de OpenAI. Por favor configúrala en la sección de Configuración.")
        else:
            st.warning("No se encontraron resultados.")

elif menu == "Configuración":
    st.title("⚙️ Configuración")
    st.markdown("Aquí podrás personalizar la configuración del monitor de evidencia.")
    
    # Añadir campo para OpenAI API Key
    current_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key_input = st.text_input(
        "OpenAI API Key", 
        value=current_api_key,
        type="password", 
        help="Necesario para la funcionalidad de resumen con IA"
    )
    
    if st.button("Guardar configuración"):
        # Guardar la configuración
        if api_key_input:
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key_input}")
            st.success("API Key guardada correctamente. Reinicia la aplicación para aplicar los cambios.")
            st.experimental_rerun()  # Intentar recargar la app
        else:
            st.error("Por favor ingresa una API Key válida.")
    
    st.divider()
    st.success("Más opciones de configuración disponibles próximamente.")