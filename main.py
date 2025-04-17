import streamlit as st
from PIL import Image
import os
import time
import random
import pandas as pd
import altair as alt
from streamlit_lottie import st_lottie
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.pubmed_api import buscar_pubmed
from sources.europe_pmc import buscar_europe_pmc
from utils.summarizer import resumir_texto

# Cargar variables de entorno
load_dotenv()

# Configuración general de la página
st.set_page_config(
    page_title="EvidenceWatch Pro | Monitor de Evidencia Científica",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# Función para cargar animaciones Lottie
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Cargar estilos CSS mejorados
estilos_path = "assets/estilos.css"
if os.path.exists(estilos_path):
    with open(estilos_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    # CSS por defecto si no existe el archivo
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .dashboard-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .highlight-text {
            color: #1E88E5;
            font-weight: 600;
        }
        .sidebar .sidebar-content {
            background-image: linear-gradient(#2c3e50, #1a252f);
            color: white;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #1565C0;
        }
        .search-result {
            border-left: 4px solid #1E88E5;
            padding-left: 10px;
        }
        footer {
            visibility: hidden;
        }
        </style>
        """, unsafe_allow_html=True)

# ----- SIDEBAR -----
# Mostrar logo si existe
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=180)
else:
    st.sidebar.markdown("### 🧬 EvidenceWatch Pro")

st.sidebar.markdown("---")

# Menú de navegación lateral mejorado con iconos
menu = st.sidebar.radio(
    "Navegación",
    ["🏠 Dashboard", "🔍 Búsqueda Científica", "🧪 Clinical Trials", "📊 Análisis", "⚙️ Configuración"]
)

# Mostrar información de usuario simulada
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Usuario")
st.sidebar.markdown("Dr. Usuario Premium")
st.sidebar.progress(80)
st.sidebar.caption("Plan Pro - 80% utilizado")

# Añadir un selector de fechas para filtrar resultados
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Filtros Temporales")
fecha_inicio = st.sidebar.date_input(
    "Desde",
    datetime.now() - timedelta(days=365)
)
fecha_fin = st.sidebar.date_input(
    "Hasta",
    datetime.now()
)

# Añadir filtros adicionales
st.sidebar.markdown("### 🔄 Filtros Avanzados")
filtro_tipo = st.sidebar.multiselect(
    "Tipo de contenido",
    ["Artículos", "Reviews", "Ensayos Clínicos", "Meta-análisis", "Guías Clínicas"],
    default=["Artículos", "Reviews"]
)

filtro_acceso = st.sidebar.radio(
    "Acceso",
    ["Todos", "Open Access", "Solo suscritos"]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 EvidenceWatch Pro v2.5")

# ----- MAIN CONTENT -----

# 1. DASHBOARD
if "🏠 Dashboard" in menu:
    # Header de bienvenida
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧬 EvidenceWatch Pro")
        st.markdown("""
        <div style='background-color: #e8f4fc; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <h4 style='margin:0'>Bienvenido al futuro del monitoreo de evidencia científica</h4>
            <p style='margin-top:10px; margin-bottom:0'>Manténgase actualizado con las últimas investigaciones científicas a través de nuestras herramientas de análisis avanzadas.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Cargar animación Lottie para la sección principal
        lottie_url = "https://assets6.lottiefiles.com/packages/lf20_m6cuL6.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=150, key="dashboard_animation")
        else:
            st.image("https://via.placeholder.com/150", width=150)

    # Métricas destacadas
    st.markdown("### 📈 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='dashboard-card'>
            <h3 style='margin:0; font-size:16px'>Nuevas Publicaciones</h3>
            <h2 style='margin:0; color:#1E88E5; font-size:28px'>574</h2>
            <p style='margin:0; color:green; font-size:12px'>↑ 12% desde ayer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='dashboard-card'>
            <h3 style='margin:0; font-size:16px'>Ensayos Clínicos</h3>
            <h2 style='margin:0; color:#1E88E5; font-size:28px'>128</h2>
            <p style='margin:0; color:orange; font-size:12px'>↓ 3% esta semana</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='dashboard-card'>
            <h3 style='margin:0; font-size:16px'>Actualizaciones Guías</h3>
            <h2 style='margin:0; color:#1E88E5; font-size:28px'>12</h2>
            <p style='margin:0; color:green; font-size:12px'>↑ 2 nuevas hoy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='dashboard-card'>
            <h3 style='margin:0; font-size:16px'>Impacto Promedio</h3>
            <h2 style='margin:0; color:#1E88E5; font-size:28px'>8.4</h2>
            <p style='margin:0; color:green; font-size:12px'>↑ 0.3 este mes</p>
        </div>
        """, unsafe_allow_html=True)

    # Gráficos de tendencias simulados
    st.markdown("### 📊 Tendencias de Publicaciones")
    
    # Datos simulados para el gráfico
    chart_data = pd.DataFrame({
        'fecha': pd.date_range(start='2025-01-01', periods=90, freq='D'),
        'PubMed': [random.randint(80, 150) for _ in range(90)],
        'Europe PMC': [random.randint(60, 120) for _ in range(90)],
        'Clinical Trials': [random.randint(10, 40) for _ in range(90)]
    })
    
    # Crear gráfico de líneas con Altair
    chart = alt.Chart(chart_data.melt('fecha', var_name='fuente', value_name='publicaciones')).mark_line().encode(
        x=alt.X('fecha:T', title='Fecha'),
        y=alt.Y('publicaciones:Q', title='Número de Publicaciones'),
        color=alt.Color('fuente:N', legend=alt.Legend(title="Fuente")),
        tooltip=['fecha', 'fuente', 'publicaciones']
    ).properties(
        height=300
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Añadir temas destacados
    st.markdown("### 🔥 Temas Emergentes")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='dashboard-card'>
            <h4 style='margin:0'>Avances en Terapias GLP-1</h4>
            <p style='margin-top:10px'>Las investigaciones sobre agonistas del receptor GLP-1 para obesidad y diabetes muestran resultados prometedores en estudios a largo plazo.</p>
            <div style='display:flex; gap:5px'>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Diabetes</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Obesidad</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>GLP-1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='dashboard-card'>
            <h4 style='margin:0'>Microbioma y Enfermedades Inflamatorias</h4>
            <p style='margin-top:10px'>Nuevas publicaciones establecen conexiones entre alteraciones del microbioma y patogénesis de enfermedades inflamatorias intestinales.</p>
            <div style='display:flex; gap:5px'>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Microbioma</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Enfermedad de Crohn</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='dashboard-card'>
            <h4 style='margin:0'>Biomarcadores en Oncología</h4>
            <p style='margin-top:10px'>Avances en la detección temprana de cáncer mediante biomarcadores circulantes en sangre permiten diagnósticos más precisos.</p>
            <div style='display:flex; gap:5px'>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Oncología</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Biomarcadores</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='dashboard-card'>
            <h4 style='margin:0'>Inmunoterapias de Última Generación</h4>
            <p style='margin-top:10px'>Los ensayos clínicos fase III muestran eficacia aumentada en combinaciones de inhibidores de checkpoint para tumores sólidos avanzados.</p>
            <div style='display:flex; gap:5px'>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Inmunoterapia</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Oncología</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. BÚSQUEDA
elif "🔍 Búsqueda Científica" in menu:
    st.title("🔍 Búsqueda Científica Inteligente")
    
    # Introducción a la herramienta
    st.markdown("""
    <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
        <h4 style='margin-top:0'>Búsqueda unificada en las principales bases de datos científicas</h4>
        <p>Nuestra tecnología permite búsquedas simultáneas en PubMed, Europe PMC y otras fuentes científicas con análisis de IA integrado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario de búsqueda mejorado
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("🔎 Escriba su término de búsqueda", value="semaglutide", 
                              placeholder="Ej: semaglutide in obesity, machine learning diagnostics...")
    
    with col2:
        max_resultados = st.slider("Resultados por fuente", 5, 50, 10)
    
    # Opciones avanzadas
    with st.expander("Opciones avanzadas de búsqueda"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            idioma = st.selectbox("Idioma", ["Todos", "Inglés", "Español", "Francés", "Alemán"])
            ordenar_por = st.selectbox("Ordenar por", ["Relevancia", "Fecha (reciente)", "Fecha (antigua)", "Factor de impacto"])
        
        with col2:
            tipo_documento = st.multiselect("Tipo de documento", 
                                         ["Todos", "Artículo original", "Revisión", "Metaanálisis", "Ensayo clínico", "Guía clínica"],
                                         default=["Todos"])
            años = st.slider("Rango de años", 2000, 2025, (2020, 2025))
        
        with col3:
            solo_humanos = st.checkbox("Solo estudios en humanos", value=True)
            solo_abiertos = st.checkbox("Solo acceso abierto", value=False)
            incluir_preprints = st.checkbox("Incluir preprints", value=True)

    # Botón de búsqueda principal
    if st.button("Buscar evidencia científica", use_container_width=True):
        
        # Contenedor para mostrar el progreso de la búsqueda
        progress_container = st.empty()
        
        progress_bar = progress_container.progress(0)
        for i in range(101):
            time.sleep(0.01)  # Simular carga
            progress_bar.progress(i)
        
        progress_container.empty()
        
        # Información sobre los resultados
        st.success(f"Se encontraron 87 resultados para '{query}' en todas las fuentes")
        
        # Pestañas para organizar los resultados
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Todos los resultados", "📊 PubMed", "🌍 Europe PMC", "💡 Análisis de IA"])
        
        # Pestaña 1: Todos los resultados
        with tab1:
            # Simulación de resultados combinados
            for i in range(1, 6):
                with st.expander(f"Efficacy and safety of semaglutide in type 2 diabetes patients - Phase {i} clinical trial"):
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **Autores:** Jensen AB, Smith JR, Anderson P, et al.
                        
                        **Publicado en:** New England Journal of Medicine • {2025-i} • Factor de impacto: {round(10.5 - i*0.5, 1)}
                        
                        **Resumen:** This randomized clinical trial evaluated the efficacy and safety of semaglutide in patients with type 2 diabetes over a 52-week period. The study demonstrated significant improvements in glycemic control and weight reduction compared to placebo, with a favorable safety profile.
                        
                        **Conclusiones clave:** Semaglutide showed dose-dependent reductions in HbA1c and body weight with acceptable tolerability.
                        """)
                        
                        st.markdown("""
                        <div style='display:flex; gap:5px'>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Diabetes</span>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Semaglutide</span>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Clinical Trial</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        **PMID:** 3652891{i}
                        
                        **Citado:** {120 - i*15} veces
                        
                        **Acceso:** {'Abierto ✓' if i % 2 == 0 else 'Restringido'}
                        """)
                        
                        st.download_button(
                            label="PDF",
                            data=b"sample",
                            file_name=f"semaglutide_study_{i}.pdf",
                            mime="application/pdf",
                        )
        
        # Pestaña 2: PubMed
        with tab2:
            if query:
                with st.spinner("Consultando PubMed..."):
                    resultados_pubmed = buscar_pubmed(query, max_resultados)
                if resultados_pubmed:
                    for r in resultados_pubmed:
                        with st.expander(r["Título"]):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**Autores:** {r['Autores']}")
                                st.markdown(f"**Fuente:** {r['Fuente']}")
                                st.markdown(f"**Resumen original:**\n\n{r['Resumen']}")
                            
                            with col2:
                                st.markdown(f"**PMID:** {r['PMID']}")
                                # Añadir botón para guardar o exportar
                                st.button("⭐ Guardar", key=f"save_pubmed_{r['PMID']}")
                                st.button("📤 Exportar", key=f"export_pubmed_{r['PMID']}")
                            
                            # Resumen por IA
                            st.markdown("**🧠 Análisis de IA:**")
                            with st.spinner("Analizando contenido..."):
                                resumen_ia = resumir_texto(r["Resumen"])
                                st.info(resumen_ia)
                else:
                    st.warning("No se encontraron resultados en PubMed.")
        
        # Pestaña 3: Europe PMC
        with tab3:
            if query:
                with st.spinner("Consultando Europe PMC..."):
                    resultados_epmc = buscar_europe_pmc(query, max_resultados)
                if resultados_epmc:
                    for e in resultados_epmc:
                        with st.expander(e["Título"]):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**Fuente:** {e['Fuente']}")
                                st.markdown(f"**Tipo de publicación:** {e['Tipo']}")
                                # Añadir enlaces a texto completo cuando estén disponibles
                                st.markdown(f"**Enlace:** [Ver artículo completo]({e['Enlace']})")
                            
                            with col2:
                                st.markdown(f"**ID:** {e['ID']}")
                                # Añadir botones de acción
                                st.button("⭐ Guardar", key=f"save_epmc_{e['ID']}")
                                st.button("📤 Exportar", key=f"export_epmc_{e['ID']}")
                else:
                    st.warning("No se encontraron resultados en Europe PMC.")
        
        # Pestaña 4: Análisis de IA
        with tab4:
            st.subheader("🧠 Análisis de tendencias por IA")
            
            # Simulación de análisis de IA
            st.markdown("""
            <div style='background-color:#f0f7ff; padding:20px; border-radius:5px; margin-bottom:20px;'>
                <h4 style='margin-top:0'>Insights sobre semaglutide</h4>
                <p>Basado en el análisis de 87 publicaciones recientes, encontramos las siguientes tendencias:</p>
                <ul>
                    <li><strong>Efectividad:</strong> El 92% de los estudios reportan efectividad significativa en reducción de peso y control glucémico.</li>
                    <li><strong>Poblaciones:</strong> La mayoría de estudios se han realizado en poblaciones de América del Norte y Europa, con creciente interés en diversidad étnica.</li>
                    <li><strong>Efectos secundarios:</strong> Los efectos gastrointestinales son los más comunes, con tendencia a disminuir tras las primeras semanas.</li>
                    <li><strong>Comparaciones:</strong> Superioridad demostrada frente a otros GLP-1 RA en términos de reducción de HbA1c y peso.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico de tendencias
            st.subheader("Evolución de las publicaciones")
            chart_data = pd.DataFrame({
                'Año': [2020, 2021, 2022, 2023, 2024, 2025],
                'Publicaciones': [12, 18, 29, 47, 68, 23]
            })
            
            chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x='Año:O',
                y='Publicaciones:Q',
                tooltip=['Año', 'Publicaciones']
            ).properties(
                height=300
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            # Temas relacionados
            st.subheader("Conceptos relacionados")
            st.markdown("""
            <div style='display:flex; flex-wrap:wrap; gap:10px'>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>GLP-1 (95%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Obesidad (87%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Diabetes tipo 2 (85%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Pérdida de peso (78%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Control glucémico (72%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Efectos adversos (65%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Cardiovascular (58%)</span>
                <span style='background-color:#e1f5fe; color:#0277bd; padding:8px 15px; border-radius:20px; font-size:14px'>Liraglutide (52%)</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Fortaleza de la evidencia
            st.subheader("Evaluación de la calidad de evidencia")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div style='text-align:center'>
                    <h3 style='margin:0; font-size:16px'>Ensayos clínicos</h3>
                    <div style='font-size:24px; color:#2e7d32; font-weight:bold'>A+</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='text-align:center'>
                    <h3 style='margin:0; font-size:16px'>Meta-análisis</h3>
                    <div style='font-size:24px; color:#2e7d32; font-weight:bold'>A</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='text-align:center'>
                    <h3 style='margin:0; font-size:16px'>Estudios observacionales</h3>
                    <div style='font-size:24px; color:#f9a825; font-weight:bold'>B+</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div style='text-align:center'>
                    <h3 style='margin:0; font-size:16px'>Calidad general</h3>
                    <div style='font-size:24px; color:#2e7d32; font-weight:bold'>A</div>
                </div>
                """, unsafe_allow_html=True)

