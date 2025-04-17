import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.pubmed_api import buscar_pubmed
from sources.europe_pmc import buscar_europe_pmc
from utils.summarizer import resumir_texto




# Cargar variables de entorno
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
    st.title("🔍 Búsqueda unificada: PubMed + Europe PMC")

    with st.form("form_busqueda"):
        query = st.text_input("🔎 Término de búsqueda", value="semaglutide")
        max_resultados = st.slider("Resultados a mostrar por fuente", 5, 50, 10)
        submitted = st.form_submit_button("Buscar")

    if submitted and query:
        ### 1. PubMed ###
        st.subheader("📖 Resultados en PubMed")
        with st.spinner("Consultando PubMed..."):
            resultados_pubmed = buscar_pubmed(query, max_resultados)

        if resultados_pubmed:
            for r in resultados_pubmed:
                with st.expander(r["Título"]):
                    st.markdown(f"**PMID:** {r['PMID']}")
                    st.markdown(f"**Autores:** {r['Autores']}")
                    st.markdown(f"**Fuente:** {r['Fuente']}")
                    st.markdown(f"**Resumen original:**\n\n{r['Resumen']}")
                    st.markdown("**🧠 Resumen generado por IA:**")
                    with st.spinner("Resumiendo..."):
                        resumen_ia = resumir_texto(r["Resumen"])
                        st.info(resumen_ia)
        else:
            st.warning("No se encontraron resultados en PubMed.")

        st.divider()

        ### 2. Europe PMC ###
        st.subheader("🌍 Resultados en Europe PMC")
        with st.spinner("Consultando Europe PMC..."):
            resultados_epmc = buscar_europe_pmc(query, max_resultados)

        if resultados_epmc:
            for e in resultados_epmc:
                with st.expander(e["Título"]):
                    st.markdown(f"**ID:** [{e['ID']}]({e['Enlace']})")
                    st.markdown(f"**Fuente:** {e['Fuente']}")
                    st.markdown(f"**Tipo de publicación:** {e['Tipo']}")
        else:
            st.warning("No se encontraron resultados en Europe PMC.")




elif menu == "Configuración":
    st.title("⚙️ Configuración")
    st.markdown("Aquí podrás personalizar la configuración del monitor de evidencia.")
    st.success("Próximamente podrás configurar opciones de resumen, exportación y alertas por correo.")
