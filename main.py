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

# 3. CLINICAL TRIALS
elif "🧪 Clinical Trials" in menu:
    st.title("🧪 Monitoreo de Ensayos Clínicos")
    
    # Introducción a la sección
    st.markdown("""
    <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
        <h4 style='margin-top:0'>Seguimiento en tiempo real de ensayos clínicos globales</h4>
        <p>Monitoree los ensayos clínicos más relevantes, sus actualizaciones y resultados preliminares en todo el mundo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros para ensayos clínicos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        area_terapeutica = st.selectbox(
            "Área terapéutica",
            ["Todas", "Oncología", "Cardiología", "Endocrinología", "Neurología", "Inmunología", "Enfermedades raras"]
        )
    
    with col2:
        fase_ensayo = st.multiselect(
            "Fase del ensayo",
            ["I", "II", "III", "IV"],
            default=["III", "IV"]
        )
    
    with col3:
        estado_ensayo = st.multiselect(
            "Estado",
            ["Reclutando", "Activo, no reclutando", "Completado", "No iniciado"],
            default=["Reclutando", "Activo, no reclutando"]
        )
    
    # Búsqueda específica para ensayos
    query_trials = st.text_input("🔎 Buscar ensayos clínicos", value="", 
                              placeholder="Ej: semaglutide, cáncer de páncreas, hipertensión resistente...")
    
    if st.button("Buscar ensayos clínicos", use_container_width=True):
        st.success(f"Se encontraron 42 ensayos clínicos que coinciden con sus criterios")
        
        # Resultados ensayos clínicos
        for i in range(1, 6):
            with st.expander(f"SEMAGOLD-{i}: Evaluación de semaglutide oral en pacientes con DMT2 y enfermedad cardiovascular"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **ID:** NCT0{random.randint(1000000, 9999999)}
                    
                    **Patrocinador:** {'Industria Farmacéutica' if i % 2 == 0 else 'Centro Médico Universitario'}
                    
                    **Fase:** {random.choice(['II', 'III', 'IV'])}
                    
                    **Estado:** {random.choice(['Reclutando', 'Activo, no reclutando'])}
                    
                    **Sitios activos:** {random.randint(10, 50)} en {random.randint(3, 15)} países
                    
                    **Intervención principal:** Semaglutide oral {random.choice(['10mg', '15mg', '20mg'])} una vez al día vs placebo
                    
                    **Actualización reciente:** {random.choice(['Resultados preliminares', 'Cambio en criterios de inclusión', 'Nuevo sitio de estudio', 'Reporte de seguridad'])}
                    """)
                    
                with col2:
                    st.markdown(f"""
                    **Participantes:** {random.randint(1000, 5000)}
                    
                    **Fecha inicio:** {random.choice(['Ene', 'Feb', 'Mar', 'Abr'])} 202{random.randint(3, 5)}
                    
                    **Fecha estimada conclusión:** {random.choice(['Jun', 'Jul', 'Ago', 'Sep', 'Oct'])} 202{random.randint(5, 7)}
                    """)
                    
                    # Botones de acción
                    st.button("📌 Seguir", key=f"follow_trial_{i}")
                    st.button("📑 Protocolo", key=f"protocol_trial_{i}")
                
                # Mostrar información adicional sobre el ensayo
                st.markdown("##### Criterios de inclusión principales:")
                st.markdown("""
                - Pacientes adultos (>18 años)
                - Diabetes mellitus tipo 2 diagnosticada
                - HbA1c entre 7.0% y 10.5%
                - Enfermedad cardiovascular aterosclerótica establecida
                - IMC ≥25 kg/m²
                """)
                
                # Mapa de sitios de estudio
                st.markdown("##### Distribución de sitios de estudio:")
                # Simulación de datos para el mapa
                trial_sites = pd.DataFrame({
                    'lat': [random.uniform(25, 60) for _ in range(15)],
                    'lon': [random.uniform(-120, 30) for _ in range(15)],
                    'sitio': [f'Centro {random.randint(1, 100)}' for _ in range(15)],
                    'pacientes_reclutados': [random.randint(10, 100) for _ in range(15)]
                })
                
                st.map(trial_sites)
                
                # Línea de tiempo del ensayo
                st.markdown("##### Línea de tiempo del ensayo:")
                
                timeline_chart = alt.Chart(pd.DataFrame({
                    'Fase': ['Diseño', 'Inicio', 'Reclutamiento', 'Tratamiento', 'Análisis', 'Resultados'],
                    'Inicio': [0, 3, 6, 8, 24, 30],
                    'Fin': [3, 6, 18, 24, 30, 36],
                    'Estado': ['Completado', 'Completado', 'En progreso', 'Planificado', 'Planificado', 'Planificado']
                })).mark_bar().encode(
                    x='Inicio',
                    x2='Fin',
                    y='Fase',
                    color=alt.Color('Estado', scale=alt.Scale(
                        domain=['Completado', 'En progreso', 'Planificado'],
                        range=['#2ecc71', '#3498db', '#95a5a6']
                    ))
                ).properties(height=200)
                
                st.altair_chart(timeline_chart, use_container_width=True)
                
                # Resultados preliminares cuando estén disponibles
                if i <= 2:
                    st.markdown("##### Resultados preliminares disponibles:")
                    
                    results_data = pd.DataFrame({
                        'Grupo': ['Semaglutide', 'Placebo'],
                        'Reducción HbA1c (%)': [1.4 + random.uniform(-0.2, 0.2), 0.3 + random.uniform(-0.1, 0.1)],
                        'Reducción peso (kg)': [4.5 + random.uniform(-0.5, 0.5), 0.8 + random.uniform(-0.2, 0.2)],
                        'Eventos CV (%)': [3.2 + random.uniform(-0.5, 0.5), 5.1 + random.uniform(-0.5, 0.5)]
                    })
                    
                    st.dataframe(results_data, use_container_width=True)
                    
                    # Comentario analítico
                    st.info("💡 **Análisis IA:** Los datos preliminares sugieren una eficacia significativa en reducción de HbA1c y peso comparado con placebo, con tendencia a reducción de eventos cardiovasculares que necesita confirmación al completar el estudio.")

# 4. ANÁLISIS
elif "📊 Análisis" in menu:
    st.title("📊 Análisis Avanzado de Evidencia")
    
    # Introducción a la sección
    st.markdown("""
    <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
        <h4 style='margin-top:0'>Herramientas de análisis impulsadas por IA</h4>
        <p>Extraiga insights significativos de la literatura científica mediante análisis estadísticos y visualizaciones avanzadas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de tipo de análisis
    tipo_analisis = st.radio(
        "Seleccione tipo de análisis",
        ["Comparativo", "Meta-análisis", "Tendencias temporales", "Network Analysis"],
        horizontal=True
    )
    
    # Demostración de herramienta de análisis comparativo
    if tipo_analisis == "Comparativo":
        st.subheader("Análisis Comparativo de Tratamientos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tratamiento1 = st.selectbox(
                "Tratamiento 1",
                ["Semaglutide", "Liraglutide", "Tirzepatide", "Empagliflozin", "Canagliflozin"]
            )
        
        with col2:
            tratamiento2 = st.selectbox(
                "Tratamiento 2",
                ["Tirzepatide", "Semaglutide", "Liraglutide", "Dulaglutide", "Placebo"],
                index=1
            )
        
        endpoint = st.multiselect(
            "Endpoints a comparar",
            ["Reducción HbA1c", "Pérdida de peso", "Eventos cardiovasculares", "Eventos adversos", "Abandonos"],
            default=["Reducción HbA1c", "Pérdida de peso"]
        )
        
        # Botón para ejecutar análisis
        if st.button("Ejecutar análisis comparativo", use_container_width=True):
            st.success(f"Analizando diferencias entre {tratamiento1} y {tratamiento2} usando 17 estudios")
            
            # Forest plot simulado
            st.subheader("Forest Plot - Diferencia media en reducción de HbA1c")
            
            # Datos simulados para forest plot
            forest_data = pd.DataFrame({
                'Estudio': [f"Estudio {chr(65+i)}" for i in range(8)],
                'Año': [random.randint(2020, 2025) for _ in range(8)],
                'DiferenciaMean': [-0.3, -0.5, -0.2, -0.4, -0.6, -0.3, -0.5, -0.4],
                'LowerCI': [-0.5, -0.7, -0.4, -0.6, -0.8, -0.5, -0.7, -0.6],
                'UpperCI': [-0.1, -0.3, -0.1, -0.2, -0.4, -0.1, -0.3, -0.2],
                'Weight': [12, 15, 10, 18, 14, 11, 9, 11]
            })
            
            # Crear forest plot con Altair
            base = alt.Chart(forest_data).encode(
                y=alt.Y('Estudio:N', sort=None)
            )
            
            lines = base.mark_rule().encode(
                x=alt.X('LowerCI:Q', title='Diferencia en HbA1c (%)'),
                x2='UpperCI:Q'
            )
            
            points = base.mark_circle(size=100).encode(
                x='DiferenciaMean:Q',
                color=alt.value('black'),
                tooltip=['Estudio', 'Año', 'DiferenciaMean', 'LowerCI', 'UpperCI', 'Weight']
            )
            
            forest_chart = (lines + points).properties(height=300)
            
            st.altair_chart(forest_chart, use_container_width=True)
            
            # Gráfico de comparación de barras
            st.subheader("Comparación de endpoints")
            
            comparison_data = pd.DataFrame({
                'Endpoint': ['Reducción HbA1c (%)', 'Pérdida de peso (kg)', 'Reducción PAS (mmHg)', 'Eventos CV (%)'],
                tratamiento1: [1.6, 5.2, 3.8, 3.2],
                tratamiento2: [1.2, 3.6, 2.9, 3.5],
            }).melt('Endpoint', var_name='Tratamiento', value_name='Valor')
            
            bar_chart = alt.Chart(comparison_data).mark_bar().encode(
                x=alt.X('Tratamiento:N'),
                y=alt.Y('Valor:Q'),
                color=alt.Color('Tratamiento:N', legend=None),
                column=alt.Column('Endpoint:N'),
                tooltip=['Tratamiento', 'Valor']
            ).properties(
                width=150
            )
            
            st.altair_chart(bar_chart, use_container_width=True)
            
            # Tabla de NNT y NNH
            st.subheader("Números Necesarios a Tratar (NNT) y para Dañar (NNH)")
            
            nnt_data = pd.DataFrame({
                'Resultado': ['Reducción HbA1c >1%', 'Pérdida >5% peso corporal', 'Prevención evento CV', 
                             'Náusea', 'Vómito', 'Discontinuación por EA'],
                'NNT/NNH': [4, 6, 32, -12, -18, -42],
                'IC 95%': ['3-5', '5-8', '22-68', '-9 a -16', '-14 a -25', '-30 a -86'],
                'Tipo': ['Beneficio', 'Beneficio', 'Beneficio', 'Daño', 'Daño', 'Daño']
            })
            
            def highlight_rows(row):
                if row['Tipo'] == 'Beneficio':
                    return ['background-color: #d4edda'] * len(row)
                else:
                    return ['background-color: #f8d7da'] * len(row)
            
            st.dataframe(nnt_data.style.apply(highlight_rows, axis=1), use_container_width=True)
            
            # Análisis de calidad de la evidencia
            st.subheader("Evaluación de calidad de la evidencia")
            
            grade_data = pd.DataFrame({
                'Dominio': ['Riesgo de sesgo', 'Inconsistencia', 'Evidencia indirecta', 'Imprecisión', 'Sesgo de publicación', 'Calidad global'],
                'Evaluación': ['Bajo', 'Moderado', 'Bajo', 'Bajo', 'No detectado', 'Alta'],
                'Explicación': [
                    'La mayoría de estudios fueron doble ciego con bajo riesgo de sesgo',
                    'Heterogeneidad moderada (I²=42%)',
                    'Comparaciones directas disponibles',
                    'Intervalos de confianza estrechos',
                    'Análisis de funnel plot sin asimetrías significativas',
                    'Evidencia de alta calidad para la comparación entre tratamientos'
                ]
            })
            
            st.table(grade_data)
            
            # Comentario analítico
            st.info("""
            💡 **Conclusión del análisis IA:**
            
            La evidencia disponible indica que Semaglutide proporciona reducciones estadísticamente superiores en HbA1c y peso corporal comparado con Liraglutide. Las diferencias en beneficios cardiovasculares no son estadísticamente significativas. El perfil de eventos adversos es similar entre ambos tratamientos, con mayor probabilidad de síntomas gastrointestinales en el grupo de Semaglutide, pero con tasas de discontinuación comparables.
            
            Se recomienda considerar Semaglutide como opción preferente cuando el objetivo principal sea la reducción de peso o el control glucémico intensivo, mientras que ambas opciones muestran beneficios cardiovasculares comparables.
            """)
    
    # Demostración de meta-análisis
    elif tipo_analisis == "Meta-análisis":
        st.subheader("Generador de Meta-análisis")
        
        st.markdown("""
        Esta herramienta permite realizar meta-análisis instantáneos a partir de la literatura científica actualizada.
        Seleccione los parámetros para su análisis:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            intervencion = st.selectbox(
                "Intervención",
                ["GLP-1 RA", "SGLT2i", "DPP-4i", "Insulina", "Metformina"]
            )
            
            poblacion = st.selectbox(
                "Población",
                ["DMT2", "Obesidad", "Insuficiencia cardíaca", "Enfermedad renal crónica"]
            )
        
        with col2:
            desenlace = st.selectbox(
                "Desenlace principal",
                ["Mortalidad CV", "HbA1c", "Peso corporal", "Eventos renales", "MACE"]
            )
            
            modelo = st.radio(
                "Modelo estadístico",
                ["Efectos aleatorios", "Efectos fijos"],
                horizontal=True
            )
        
        # Opciones avanzadas
        with st.expander("Opciones avanzadas"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                heterogeneidad = st.checkbox("Análisis de heterogeneidad", value=True)
                metaregresion = st.checkbox("Meta-regresión", value=False)
            
            with col2:
                sesgo_publicacion = st.checkbox("Evaluación de sesgo de publicación", value=True)
                analisis_sensibilidad = st.checkbox("Análisis de sensibilidad", value=True)
            
            with col3:
                subgrupos = st.multiselect(
                    "Análisis de subgrupos",
                    ["Edad", "Sexo", "Duración diabetes", "Comorbilidades", "HbA1c basal"],
                    default=["Edad", "HbA1c basal"]
                )
        
        # Botón para ejecutar meta-análisis
        if st.button("Ejecutar meta-análisis", use_container_width=True):
            with st.spinner("Analizando estudios..."):
                time.sleep(2)  # Simular procesamiento
            
            st.success(f"Meta-análisis completado | 23 estudios incluidos | 58,721 participantes")
            
            # Resultados del meta-análisis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Forest Plot - Efectos sobre Mortalidad CV")
                
                # Imagen placeholder para forest plot
                st.image("https://via.placeholder.com/700x400?text=Forest+Plot", use_column_width=True)
            
            with col2:
                st.subheader("Resultados principales")
                st.markdown("""
                **Efecto global:**
                - RR: 0.82 (IC 95%: 0.74-0.91)
                - p < 0.001
                
                **Heterogeneidad:**
                - I² = 37%
                - Q = 34.8 (p = 0.07)
                
                **NNT:** 42 (IC 95%: 32-67)
                """)
            
            # Gráfico de embudo (funnel plot)
            st.subheader("Funnel Plot - Evaluación de sesgo de publicación")
            
            # Datos simulados para funnel plot
            funnel_data = pd.DataFrame({
                'LogRR': [-0.3 + random.uniform(-0.2, 0.2) for _ in range(23)],
                'SE': [random.uniform(0.05, 0.5) for _ in range(23)],
                'Estudio': [f"Estudio {i+1}" for i in range(23)]
            })
            
            funnel_chart = alt.Chart(funnel_data).mark_circle(size=80).encode(
                x=alt.X('LogRR:Q', title='Log Risk Ratio', scale=alt.Scale(domain=[-1, 0.4])),
                y=alt.Y('SE:Q', title='Standard Error', scale=alt.Scale(domain=[0.5, 0], reverse=True)),
                tooltip=['Estudio', 'LogRR', 'SE']
            ).properties(
                width=700,
                height=400
            )
            
            # Línea vertical para el efecto promedio
            vline = alt.Chart(pd.DataFrame({'x': [-0.198]})).mark_rule(color='red').encode(x='x')
            
            # Líneas de embudo
            limit_data = pd.DataFrame({
                'LogRR': [-0.198 - 1.96 * x, -0.198 + 1.96 * x, None] for x in 
                         [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            }).melt(var_name='limit', value_name='LogRR')
            
            limit_data['SE'] = limit_data['limit'].map({
                f"-0.198 - 1.96 * {x}": x for x in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            } | {
                f"-0.198 + 1.96 * {x}": x for x in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            } | {
                'None': None
            })
            
            limit_data = limit_data.dropna()
            
            funnel_lines = alt.Chart(limit_data).mark_line(
                color='blue', opacity=0.5, strokeDash=[5, 5]
            ).encode(
                x='LogRR:Q',
                y='SE:Q'
            )
            
            st.altair_chart(vline + funnel_chart + funnel_lines, use_container_width=True)
            
            # Análisis de subgrupos
            st.subheader("Análisis de subgrupos")
            
            subgroup_data = pd.DataFrame({
                'Subgrupo': ['Global', '≤65 años', '>65 años', 'HbA1c ≤8%', 'HbA1c >8%', 'Con ECV', 'Sin ECV'],
                'RR': [0.82, 0.84, 0.76, 0.88, 0.75, 0.72, 0.91],
                'Lower': [0.74, 0.75, 0.65, 0.78, 0.67, 0.63, 0.82],
                'Upper': [0.91, 0.95, 0.89, 0.99, 0.84, 0.83, 1.02],
                'p_interaction': ['', '0.21', '', '0.03', '', '0.001', ''],
                'Significativo': [True, True, True, True, True, True, False]
            })
            
            # Crear gráfico de subgrupos con Altair
            base = alt.Chart(subgroup_data).encode(
                y=alt.Y('Subgrupo:N', sort=None)
            )
            
            lines = base.mark_rule().encode(
                x=alt.X('Lower:Q', title='Risk Ratio (IC 95%)'),
                x2='Upper:Q',
                color=alt.Color('Significativo:N', scale=alt.Scale(
                    domain=[True, False],
                    range=['#1E88E5', '#ccc']
                ), legend=None)
            )
            
            points = base.mark_circle(size=100).encode(
                x='RR:Q',
                color=alt.value('black'),
                tooltip=['Subgrupo', 'RR', 'Lower', 'Upper', 'p_interaction']
            )
            
            # Línea vertical en RR=1
            vline = alt.Chart(pd.DataFrame({'x': [1]})).mark_rule(
                color='red', 
                strokeDash=[5, 5]
            ).encode(x='x')
            
            subgroup_chart = (vline + lines + points).properties(height=300)
            
            st.altair_chart(subgroup_chart, use_container_width=True)
            
            # Tabla de p-interacción
            st.markdown("**Valores p para interacción entre subgrupos:**")
            interaction_data = pd.DataFrame({
                'Subgrupo': ['Edad (≤65 vs >65)', 'HbA1c basal (≤8% vs >8%)', 'ECV basal (sí vs no)'],
                'Valor p': ['0.21', '0.03', '0.001'],
                'Significancia': ['No significativo', 'Significativo', 'Altamente significativo']
            })
            
            st.table(interaction_data)
            
            # Conclusiones del meta-análisis
            st.info("""
            💡 **Conclusiones del meta-análisis:**
            
            Este meta-análisis de 23 estudios con 58,721 participantes demuestra que los GLP-1 RA reducen significativamente la mortalidad cardiovascular en pacientes con DMT2 (RR 0.82, IC 95% 0.74-0.91, p<0.001).
            
            El análisis de subgrupos revela:
            1. Mayor beneficio en pacientes con HbA1c >8% vs ≤8% (p-interacción=0.03)
            2. Efecto más pronunciado en pacientes con enfermedad cardiovascular establecida (p-interacción=0.001)
            3. Tendencia a mayor beneficio en >65 años sin alcanzar significancia estadística
            
            La evaluación de sesgo de publicación no mostró asimetría significativa en el funnel plot, sugiriendo ausencia de sesgo de publicación importante. La heterogeneidad entre estudios fue moderada (I²=37%).
            
            **Implicaciones clínicas:** Los GLP-1 RA deberían considerarse preferentemente en pacientes con DMT2 y enfermedad cardiovascular establecida, especialmente aquellos con control glucémico subóptimo.
            """)

    # Demostración tendencias temporales
    elif tipo_analisis == "Tendencias temporales":
        st.subheader("Análisis de Tendencias Temporales en Investigación")
        
        st.markdown("""
        Explore cómo evolucionan las tendencias de investigación científica a lo largo del tiempo.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            area_investigacion = st.selectbox(
                "Área de investigación",
                ["Diabetes", "Oncología", "Cardiología", "Neurología", "Inmunología"]
            )
        
        with col2:
            periodo = st.slider(
                "Periodo de análisis",
                min_value=2000,
                max_value=2025,
                value=(2010, 2025)
            )
        
        temas_interes = st.multiselect(
            "Temas de interés",
            ["GLP-1", "SGLT2", "Inmunoterapia", "Inteligencia Artificial", "Terapia génica", "Medicina de precisión"],
            default=["GLP-1", "SGLT2"]
        )
        
        # Botón para ejecutar análisis de tendencias
        if st.button("Analizar tendencias", use_container_width=True):
            # Simular datos de tendencias
            años = list(range(2010, 2026))
            
            # Datos de publicaciones por año y tema
            trend_data = pd.DataFrame({
                'Año': años * len(temas_interes),
                'Tema': [tema for tema in temas_interes for _ in años],
                'Publicaciones': [
                    int(100 * (1 + 0.2 * (año - 2010) + random.uniform(-0.05, 0.05))) if tema == "GLP-1" else
                    int(50 * (1 + 0.4 * (año - 2015) + random.uniform(-0.05, 0.05))) if tema == "SGLT2" else
                    int(30 * (1 + 0.5 * (año - 2010) + random.uniform(-0.05, 0.05)))
                    for tema in temas_interes for año in años
                ]
            })
            
            # Filtrar por el periodo seleccionado
            trend_data = trend_data[(trend_data['Año'] >= periodo[0]) & (trend_data['Año'] <= periodo[1])]
            
            # Gráfico de tendencias
            st.subheader(f"Evolución de publicaciones en {area_investigacion} ({periodo[0]}-{periodo[1]})")
            
            trend_chart = alt.Chart(trend_data).mark_line(point=True).encode(
                x=alt.X('Año:O', title='Año'),
                y=alt.Y('Publicaciones:Q', title='Número de publicaciones'),
                color=alt.Color('Tema:N', legend=alt.Legend(title="Tema")),
                tooltip=['Año', 'Tema', 'Publicaciones']
            ).properties(
                height=400
            ).interactive()
            
            st.altair_chart(trend_chart, use_container_width=True)
            
            # Análisis de citas e impacto
            st.subheader("Análisis de impacto por tema")
            
            # Simular datos de impacto
            impact_data = pd.DataFrame({
                'Tema': temas_interes,
                'Publicaciones': [
                    sum(trend_data[trend_data['Tema']
                'Tema': temas_interes,
                'Publicaciones': [
                    sum(trend_data[trend_data['Tema'] == tema]['Publicaciones']) 
                    for tema in temas_interes
                ],
                'Citas promedio': [
                    round(random.uniform(15, 35), 1) for _ in temas_interes
                ],
                'Factor impacto': [
                    round(random.uniform(3.5, 8.2), 2) for _ in temas_interes
                ],
                'Crecimiento anual (%)': [
                    round(random.uniform(8, 25), 1) for _ in temas_interes
                ]
            })
            
            st.dataframe(impact_data, use_container_width=True)
            
            # Gráfico de burbujas para visualizar impacto
            st.subheader("Mapa de impacto científico")
            
            # Datos para gráfico de burbujas
            bubble_data = pd.DataFrame({
                'Tema': temas_interes * 3,
                'Año': [2015, 2015] + [2020, 2020] + [2025, 2025],
                'Publicaciones': [
                    int(random.uniform(100, 200)) for _ in range(len(temas_interes) * 3)
                ],
                'Citas': [
                    int(random.uniform(500, 5000)) for _ in range(len(temas_interes) * 3)
                ],
                'Impacto': [
                    round(random.uniform(2, 15), 1) for _ in range(len(temas_interes) * 3)
                ]
            })
            
            bubble_chart = alt.Chart(bubble_data).mark_circle().encode(
                x=alt.X('Publicaciones:Q', title='Número de publicaciones'),
                y=alt.Y('Citas:Q', title='Número de citas'),
                size=alt.Size('Impacto:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(title="Factor de impacto")),
                color=alt.Color('Tema:N', legend=alt.Legend(title="Tema")),
                tooltip=['Tema', 'Año', 'Publicaciones', 'Citas', 'Impacto']
            ).properties(
                height=500
            ).interactive()
            
            st.altair_chart(bubble_chart, use_container_width=True)
            
            # Análisis de colaboraciones
            st.subheader("Redes de colaboración global")
            
            # Simular datos de colaboración internacional
            countries = ['Estados Unidos', 'China', 'Reino Unido', 'Alemania', 'Japón', 'Francia', 'Canadá', 'Australia']
            connections = []
            
            for i in range(len(countries)):
                for j in range(i+1, len(countries)):
                    if random.random() > 0.3:  # 70% de probabilidad de conexión
                        strength = random.randint(5, 30)
                        connections.append({
                            'source': countries[i],
                            'target': countries[j],
                            'strength': strength
                        })
            
            # Visualizar la red de colaboración (placeholder - en producción usaría PyVis o NetworkX)
            st.markdown("""
            En una implementación completa, aquí se mostraría un gráfico interactivo de redes de colaboración
            entre instituciones y países en el campo seleccionado.
            """)
            
            # Tabla de colaboraciones
            collab_data = pd.DataFrame(connections)
            
            st.dataframe(collab_data, use_container_width=True)
            
            # Análisis de tendencias emergentes
            st.subheader("Temas emergentes identificados")
            
            emerging_topics = [
                {"tema": "Receptores GLP-1 de administración oral", "crecimiento": "+127%", "año_emergencia": 2023},
                {"tema": "Combinaciones GLP-1/GIP", "crecimiento": "+95%", "año_emergencia": 2022},
                {"tema": "Terapias con células madre para diabetes", "crecimiento": "+62%", "año_emergencia": 2024},
                {"tema": "Inteligencia artificial en endocrinología", "crecimiento": "+218%", "año_emergencia": 2021}
            ]
            
            for i, topic in enumerate(emerging_topics):
                st.markdown(f"""
                <div style="background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:10px;">
                    <h5 style="margin-top:0">{topic['tema']}</h5>
                    <p><strong>Crecimiento anual:</strong> {topic['crecimiento']} | <strong>Año de emergencia:</strong> {topic['año_emergencia']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Resumen generado por IA
            st.info("""
            💡 **Análisis de tendencias IA:**
            
            En el campo de la diabetes, se observa un crecimiento constante en investigación de agonistas del receptor GLP-1, con un aumento exponencial a partir de 2018, coincidiendo con la publicación de resultados cardiovasculares favorables.
            
            Los inhibidores SGLT2 muestran una tendencia de crecimiento aún más pronunciada desde 2015, probablemente impulsada por sus beneficios cardiovasculares y renales descubiertos en ensayos pivotales.
            
            El análisis de co-citación sugiere una creciente convergencia entre investigación en diabetes, obesidad y cardiología, reflejando un enfoque más integral en el manejo cardiometabólico.
            
            Las colaboraciones internacionales han aumentado un 42% en el período analizado, con una red especialmente fuerte entre instituciones de EE.UU., Reino Unido y Alemania.
            
            Los temas emergentes con mayor potencial disruptivo incluyen los agonistas duales/triples GLP-1/GIP, nuevas formulaciones orales y aplicaciones de inteligencia artificial en medicina de precisión para diabetes.
            """)

    # Demostración de análisis de redes
    elif tipo_analisis == "Network Analysis":
        st.subheader("Network Analysis de Evidencia Científica")
        
        st.markdown("""
        Esta herramienta permite visualizar las interrelaciones entre publicaciones, autores, instituciones y conceptos científicos.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            concepto_central = st.selectbox(
                "Concepto central",
                ["Diabetes tipo 2", "Alzheimer", "Cáncer de páncreas", "Obesidad", "COVID-19"]
            )
        
        with col2:
            profundidad_red = st.slider(
                "Profundidad de análisis",
                min_value=1,
                max_value=4,
                value=2,
                help="Nivel de expansión de la red desde el concepto central"
            )
        
        tipo_red = st.radio(
            "Tipo de red a analizar",
            ["Conceptos relacionados", "Co-citación de autores", "Colaboración institucional"],
            horizontal=True
        )
        
        # Botón para ejecutar análisis de red
        if st.button("Generar análisis de red", use_container_width=True):
            st.success(f"Analizando red de {tipo_red} para {concepto_central}")
            
            # Simular visualización de red
            st.image("https://via.placeholder.com/800x500?text=Network+Analysis+Visualization", use_column_width=True)
            
            # Métricas de red
            st.subheader("Métricas de la red")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Nodos", "284")
            with col2:
                st.metric("Conexiones", "1,240")
            with col3:
                st.metric("Centralidad promedio", "3.2")
            with col4:
                st.metric("Densidad", "0.042")
            
            # Nodos principales
            st.subheader("Nodos principales por centralidad")
            
            # Simular datos de nodos principales
            top_nodes = pd.DataFrame({
                'Nodo': [
                    "Resistencia a insulina", "Obesidad", "Disfunción mitocondrial", 
                    "Inflamación crónica", "Microbioma intestinal", "Estrés oxidativo"
                ] if tipo_red == "Conceptos relacionados" else [
                    "Smith, J.R.", "Wang, L.", "Johnson, M.K.", 
                    "Zhang, X.", "Patel, A.", "González, R.M."
                ] if tipo_red == "Co-citación de autores" else [
                    "Harvard Medical School", "Mayo Clinic", "Oxford University", 
                    "Karolinska Institute", "NIH", "Seoul National University"
                ],
                'Centralidad': [0.82, 0.76, 0.71, 0.68, 0.65, 0.63],
                'Conexiones': [58, 52, 47, 43, 41, 38]
            })
            
            st.dataframe(top_nodes, use_container_width=True)
            
            # Comunidades identificadas
            st.subheader("Comunidades identificadas en la red")
            
            # Simular datos de comunidades
            communities = [
                {"nombre": "Metabolismo energético", "nodos": 42, "densidad": 0.72},
                {"nombre": "Señalización de insulina", "nodos": 37, "densidad": 0.68},
                {"nombre": "Inflamación y citoquinas", "nodos": 31, "densidad": 0.57},
                {"nombre": "Microbioma y barrera intestinal", "nodos": 28, "densidad": 0.64},
                {"nombre": "Función mitocondrial", "nodos": 25, "densidad": 0.71}
            ] if tipo_red == "Conceptos relacionados" else [
                {"nombre": "Grupo Harvard-MIT", "nodos": 38, "densidad": 0.81},
                {"nombre": "Consorcio Europeo de Diabetes", "nodos": 35, "densidad": 0.73},
                {"nombre": "Red Asia-Pacífico", "nodos": 29, "densidad": 0.68},
                {"nombre": "Grupo Escandinavo", "nodos": 24, "densidad": 0.79}
            ]
            
            for i, comm in enumerate(communities):
                st.markdown(f"""
                <div style="background-color:#f0f7ff; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <h5 style="margin-top:0">{comm['nombre']}</h5>
                    <p><strong>Nodos:</strong> {comm['nodos']} | <strong>Densidad interna:</strong> {comm['densidad']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Evolución temporal de la red
            st.subheader("Evolución temporal de la red (2015-2025)")
            
            # Simular datos de evolución temporal
            temporal_data = pd.DataFrame({
                'Año': list(range(2015, 2026)),
                'Nodos': [80, 95, 112, 134, 156, 185, 205, 224, 248, 265, 284],
                'Conexiones': [120, 180, 267, 340, 445, 564, 684, 790, 912, 1084, 1240],
                'Densidad': [0.038, 0.040, 0.043, 0.039, 0.037, 0.041, 0.042, 0.040, 0.039, 0.042, 0.042]
            })
            
            # Crear gráfico de evolución temporal
            base = alt.Chart(temporal_data).encode(
                x=alt.X('Año:O', title='Año')
            )
            
            # Línea para nodos
            line_nodos = base.mark_line(color='blue').encode(
                y=alt.Y('Nodos:Q', title='Número de nodos', axis=alt.Axis(titleColor='blue'))
            )
            
            # Puntos para nodos
            points_nodos = base.mark_circle(color='blue', size=60).encode(
                y='Nodos:Q'
            )
            
            # Crear una segunda escala para las conexiones
            line_conexiones = base.mark_line(color='red').encode(
                y=alt.Y('Conexiones:Q', title='Número de conexiones', axis=alt.Axis(titleColor='red')),
            )
            
            points_conexiones = base.mark_circle(color='red', size=60).encode(
                y='Conexiones:Q'
            )
            
            # Combinar gráficos
            temporal_chart = alt.layer(line_nodos, points_nodos, line_conexiones, points_conexiones).resolve_scale(
                y='independent'
            ).properties(
                height=400
            ).interactive()
            
            st.altair_chart(temporal_chart, use_container_width=True)
            
            # Análisis y conclusiones
            st.info("""
            💡 **Análisis de redes IA:**
            
            El análisis de redes en torno a la Diabetes tipo 2 revela una estructura compleja con alta interconectividad entre diferentes dominios científicos.
            
            Los nodos con mayor centralidad (resistencia a insulina, obesidad y disfunción mitocondrial) actúan como puentes entre diferentes comunidades temáticas, sugiriendo su papel fundamental en la fisiopatología.
            
            La evolución temporal muestra un crecimiento exponencial de conexiones entre 2018-2022, posiblemente reflejando la integración acelerada de conocimientos entre campos tradicionalmente separados como metabolismo, inflamación y microbioma.
            
            Las cinco comunidades identificadas muestran alta cohesión interna pero también conexiones significativas entre ellas, evidenciando la naturaleza multifactorial de la enfermedad.
            
            El análisis sugiere áreas emergentes con potencial para nueva investigación en las intersecciones entre microbioma y señalización de insulina, así como entre inflamación y función mitocondrial, que presentan menos conexiones pero crecimiento reciente.
            """)

# 5. CONFIGURACIÓN
elif "⚙️ Configuración" in menu:
    st.title("⚙️ Configuración de EvidenceWatch Pro")
    
    # Panel de configuración
    st.markdown("""
    <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
        <h4 style='margin-top:0'>Personalice su experiencia</h4>
        <p>Configure sus preferencias y personalice la plataforma según sus necesidades específicas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para organizar la configuración
    tab1, tab2, tab3, tab4 = st.tabs(["🔔 Alertas", "🏷️ Etiquetas", "🔍 Búsqueda", "🔐 Cuenta"])
    
    # Tab 1: Configuración de alertas
    with tab1:
        st.subheader("Configuración de alertas y notificaciones")
        
        # Frecuencia de notificaciones
        frecuencia = st.radio(
            "Frecuencia de notificaciones",
            ["Diaria", "Cada 2-3 días", "Semanal", "Quincenal"],
            horizontal=True
        )
        
        # Canal de notificaciones
        canal = st.multiselect(
            "Canales de notificación",
            ["Email", "Aplicación móvil", "Navegador", "Slack", "Microsoft Teams"],
            default=["Email", "Aplicación móvil"]
        )
        
        # Tipos de contenido
        st.markdown("##### Tipos de contenido para alertas")
        col1, col2 = st.columns(2)
        
        with col1:
            alerta_articulos = st.checkbox("Nuevos artículos", value=True)
            alerta_guideline = st.checkbox("Actualizaciones de guías clínicas", value=True)
            alerta_trials = st.checkbox("Ensayos clínicos", value=True)
        
        with col2:
            alerta_retraction = st.checkbox("Retractaciones", value=True)
            alerta_preprint = st.checkbox("Preprints", value=False)
            alerta_conference = st.checkbox("Resúmenes de congresos", value=False)
        
        # Alertas por temas
        st.markdown("##### Configurar alertas por tema")
        
        if st.checkbox("Añadir nuevo tema de seguimiento"):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                nuevo_tema = st.text_input("Término o frase a monitorizar")
            
            with col2:
                relevancia = st.slider("Relevancia mínima", 1, 5, 3)
            
            with col3:
                st.markdown("&nbsp;")  # Espacio en blanco para alinear con el botón
                st.button("➕ Añadir")
        
        # Temas actualmente monitorizados
        st.markdown("##### Temas actualmente monitorizados")
        
        temas_seguimiento = [
            {"tema": "Semaglutide", "relevancia": 5, "frecuencia": "Diaria"},
            {"tema": "GLP-1 receptor agonists", "relevancia": 4, "frecuencia": "Diaria"},
            {"tema": "Tirzepatide", "relevancia": 4, "frecuencia": "Semanal"},
            {"tema": "Diabetes guidelines", "relevancia": 3, "frecuencia": "Semanal"}
        ]
        
        for tema in temas_seguimiento:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{tema['tema']}**")
            
            with col2:
                st.markdown(f"Relevancia: {'🟢' * tema['relevancia']}{'⚪' * (5-tema['relevancia'])}")
            
            with col3:
                st.markdown(f"{tema['frecuencia']} ✏️ 🗑️")
        
        # Guardar configuración
        st.button("💾 Guardar configuración de alertas", use_container_width=True)
    
    # Tab 2: Configuración de etiquetas
    with tab2:
        st.subheader("Gestión de etiquetas personalizadas")
        
        st.markdown("""
        Las etiquetas le permiten organizar y clasificar la literatura científica según sus necesidades.
        """)
        
        # Crear nueva etiqueta
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            nueva_etiqueta = st.text_input("Nombre de la etiqueta")
        
        with col2:
            color_etiqueta = st.color_picker("Color", "#1E88E5")
        
        with col3:
            st.markdown("&nbsp;")  # Espacio en blanco para alinear con el botón
            st.button("➕ Crear etiqueta")
        
        # Etiquetas actuales
        st.markdown("##### Etiquetas actuales")
        
        etiquetas = [
            {"nombre": "Review para journal club", "color": "#2e7d32", "articulos": 12},
            {"nombre": "Evidencia controvertida", "color": "#d32f2f", "articulos": 8},
            {"nombre": "Para meta-análisis", "color": "#7b1fa2", "articulos": 23},
            {"nombre": "Implementación clínica", "color": "#1565c0", "articulos": 17},
            {"nombre": "Metodología dudosa", "color": "#f57c00", "articulos": 5}
        ]
        
        for etiqueta in etiquetas:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="display:flex; align-items:center;">
                    <div style="width:15px; height:15px; border-radius:50%; background-color:{etiqueta['color']}; margin-right:8px;"></div>
                    <span><strong>{etiqueta['nombre']}</strong></span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"{etiqueta['articulos']} artículos")
            
            with col3:
                st.markdown("✏️ 🗑️")
        
        # Reglas automáticas
        st.markdown("##### Reglas automáticas de etiquetado")
        
        if st.checkbox("Añadir regla automática"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                condicion = st.selectbox(
                    "Condición",
                    ["Contiene en título", "Contiene en abstract", "Autor es", "Journal es", "Factor de impacto >"]
                )
                valor_condicion = st.text_input("Valor")
            
            with col2:
                etiqueta_aplicar = st.selectbox(
                    "Aplicar etiqueta",
                    [e["nombre"] for e in etiquetas]
                )
            
            with col3:
                st.markdown("&nbsp;")
                st.button("➕ Añadir regla")
        
        # Reglas existentes
        st.markdown("##### Reglas existentes")
        
        reglas = [
            {"condicion": "Contiene en título", "valor": "meta-analysis", "etiqueta": "Para meta-análisis"},
            {"condicion": "Journal es", "valor": "The Lancet", "etiqueta": "Review para journal club"},
            {"condicion": "Factor de impacto >", "valor": "10", "etiqueta": "Review para journal club"}
        ]
        
        for regla in reglas:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:8px; background-color:#f8f9fa; border-radius:5px; margin-bottom:5px;">
                <div><strong>Si</strong> [{regla['condicion']}] <strong>es</strong> "{regla['valor']}"</div>
                <div><strong>→ Aplicar</strong> "{regla['etiqueta']}"</div>
                <div>✏️ 🗑️</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Guardar configuración
        st.button("💾 Guardar configuración de etiquetas", use_container_width=True)
    
    # Tab 3: Configuración de búsqueda
    with tab3:
        st.subheader("Preferencias de búsqueda")
        
        # Fuentes preferidas
        st.markdown("##### Fuentes de datos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.checkbox("PubMed", value=True)
            st.checkbox("Web of Science", value=False)
            st.checkbox("EMBASE", value=False)
        
        with col2:
            st.checkbox("Europe PMC", value=True)
            st.checkbox("Clinical Trials", value=True)
            st.checkbox("Google Scholar", value=False)
        
        with col3:
            st.checkbox("Cochrane Library", value=True)
            st.checkbox("LILACS", value=False)
            st.checkbox("medRxiv", value=True)
        
        # Criterios de relevancia
        st.markdown("##### Criterios de relevancia para resultados")
        
        st.slider("Importancia de actualidad", 1, 10, 7)
        st.slider("Importancia de factor de impacto", 1, 10, 6)
        st.slider("Importancia de número de citas", 1, 10, 5)
        
        # Filtros predeterminados
        st.markdown("##### Filtros predeterminados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.multiselect(
                "Tipos de estudio preferidos",
                ["Meta-análisis", "Ensayo clínico", "Revisión sistemática", "Estudio observacional", "Guía clínica"],
                default=["Meta-análisis", "Ensayo clínico", "Revisión sistemática"]
            )
        
        with col2:
            st.multiselect(
                "Especies preferidas",
                ["Humanos", "Ratones", "Ratas", "Primates no humanos", "Células in vitro"],
                default=["Humanos"]
            )
        
        # Opciones de AI
        st.markdown("##### Configuración de análisis por IA")
        
        nivel_analisis = st.select_slider(
            "Nivel de análisis automático",
            options=["Básico", "Estándar", "Profundo", "Experto"],
            value="Estándar"
        )
        
        st.checkbox("Generar resúmenes automáticamente", value=True)
        st.checkbox("Extraer hallazgos clave", value=True)
        st.checkbox("Evaluar calidad metodológica", value=True)
        
        # Guardar configuración
        st.button("💾 Guardar preferencias de búsqueda", use_container_width=True)
    
    # Tab 4: Configuración de cuenta
    with tab4:
        st.subheader("Gestión de cuenta")
        
        # Información de perfil
        st.markdown("##### Información de perfil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Nombre", value="Dr. Usuario")
            st.text_input("Email", value="usuario@ejemplo.com")
            st.text_input("Institución", value="Hospital Universitario")
        
        with col2:
            st.selectbox("Especialidad", ["Endocrinología", "Cardiología", "Oncología", "Neurología", "Medicina interna"])
            st.multiselect(
                "Áreas de interés",
                ["Diabetes", "Obesidad", "Enfermedades cardiovasculares", "Trastornos tiroideos"],
                default=["Diabetes", "Obesidad"]
            )
        
        # Plan de suscripción
        st.markdown("##### Plan de suscripción")
        
        st.info("🔹 **Plan Pro** - Renovación automática el 15/12/2025")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Búsquedas avanzadas", "68/100 restantes")
        
        with col2:
            st.metric("Análisis de IA", "124/200 restantes")
        
        with col3:
            st.metric("Meta-análisis", "4/5 restantes")
        
        # Opciones de plan
        st.button("Actualizar a Plan Premium", use_container_width=True)
        
        # Exportación e importación
        st.markdown("##### Exportación e importación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("📤 Exportar biblioteca", use_container_width=True)
            st.button("📤 Exportar preferencias", use_container_width=True)
        
        with col2:
            st.file_uploader("📥 Importar biblioteca", type=["json", "xml", "ris"])
            st.file_uploader("📥 Importar preferencias", type=["json"])
        
        # Integración con herramientas
        st.markdown("##### Integración con herramientas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.checkbox("Zotero", value=True)
            st.checkbox("Mendeley", value=False)
        
        with col2:
            st.checkbox("EndNote", value=False)
            st.checkbox("Microsoft Teams", value=True)
        
        with col3:
            st.checkbox("Slack", value=False)
            st.checkbox("Notion", value=True)
        
        # Eliminar cuenta
        st.markdown("##### Peligro")
        
        with st.expander("⚠️ Eliminar cuenta"):
            st.warning("Esta acción eliminará permanentemente su cuenta y todos los datos asociados.")
            st.text_input("Escriba 'ELIMINAR' para confirmar")
            st.button("🗑️ Eliminar cuenta permanentemente")

# Añadir acción para mostrar información sobre la aplicación
with st.sidebar:
    st.markdown("---")
    if st.button("ℹ️ Acerca de EvidenceWatch"):
        st.sidebar.markdown("""
        **EvidenceWatch Pro v2.5**
        
        Desarrollado por MedTech Solutions
        
        Esta aplicación está diseñada para profesionales de la salud que desean mantenerse actualizados con la última evidencia científica relevante para su práctica clínica.
        
        © 2025 Todos los derechos reservados
        """)
