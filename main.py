import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.pubmed_api import buscar_pubmed
from utils.summarizer import resumir_texto

# Cargar variables de entorno (si se usan para otros fines)
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
menu = st.sidebar.radio("Menú principal", ["Dashboard", "Búsqueda", "Clinical Trials", "Configuración"])

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

                    st.markdown("**🧠 Resumen generado por IA (Hugging Face T5):**")
                    with st.spinner("Generando resumen con IA..."):
                        resumen_ia = resumir_texto(r["Resumen"])
                        st.info(resumen_ia)
        else:
            st.warning("No se encontraron resultados.")

elif menu == "Clinical Trials":
    st.title("🧪 Ensayos Clínicos - ClinicalTrials.gov")

    with st.form("form_trials"):
        query_trials = st.text_input("🔎 Término de búsqueda", value="semaglutide")
        max_trials = st.slider("Resultados a mostrar", 5, 50, 10)
        submitted_trials = st.form_submit_button("Buscar ensayos")

    if submitted_trials and query_trials:
        with st.spinner("Consultando ClinicalTrials.gov..."):
            ensayos = buscar_trials(query_trials, max_trials)

        if ensayos:
            st.success(f"🧪 {len(ensayos)} estudios encontrados para '{query_trials}'")

            for e in ensayos:
                with st.expander(e["Título"]):
                    st.markdown(f"**NCT ID:** [{e['NCT ID']}]({e['Enlace']})")
                    st.markdown(f"**Condición:** {e['Condición']}")
                    st.markdown(f"**Estado:** {e['Estado']}")
                    st.markdown(f"**Fase:** {e['Fase']}")
                    st.markdown(f"**País:** {e['País']}")
                    st.markdown(f"**Fecha de inicio:** {e['Fecha de inicio']}")
        else:
            st.warning("No se encontraron resultados.")


elif menu == "Configuración":
    st.title("⚙️ Configuración")
    st.markdown("Aquí podrás personalizar la configuración del monitor de evidencia.")
    st.success("Próximamente podrás configurar opciones de resumen, exportación y alertas por correo.")
