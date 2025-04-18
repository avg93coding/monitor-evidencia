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
    except BaseException:
        return None

# Cargar estilos CSS mejorados
estilos_path = "assets/estilos.css"
if os.path.exists(estilos_path):
    with open(estilos_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
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

# ------------------------------
# ESTILOS FUTURISTAS ADICIONALES
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
  body, .stApp, .stText, .stMarkdown, .stButton>button {
    font-family: 'Orbitron', sans-serif;
  }
  h1, h2, h3, h4, h5, h6 {
    letter-spacing: 1px;
  }
  h1, h2, h3 {
    color: #00e5ff;
    font-weight: 700;
  }
  p, span, li {
    color: #cfd8dc;
  }
  .main {
    background-color: #10151a;
  }
  .stApp {
    color: #eceff1;
  }
  .dashboard-card {
    background-color: #1e272e;
    box-shadow: 0 4px 12px rgba(0,255,255,0.2);
  }
  .stButton>button {
    background-color: #00e5ff;
    color: #10151a;
    font-weight: 700;
    text-transform: uppercase;
  }
  .stButton>button:hover {
    background-color: #00b8d4;
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
menu = st.sidebar.radio("Navegación",
                        ["🏠 Dashboard",
                         "🔍 Búsqueda Científica",
                         "Clinical Trials",
                         "📊 Análisis",
                         "⚙️ Configuración"])

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
        lottie_url = "https://assets6.lottiefiles.com/packages/lf20_m6cuL6.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=150, key="dashboard_animation")
        else:
            st.image("https://via.placeholder.com/150", width=150)

    # Métricas destacadas
    st.markdown("### 📈 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    # ... (tus tarjetas aquí) ...

    # Gráficos de tendencias simulados
    st.markdown("### 📊 Tendencias de Publicaciones")
    chart_data = pd.DataFrame({
        'fecha': pd.date_range(start='2025-01-01', periods=90, freq='D'),
        'PubMed': [random.randint(80, 150) for _ in range(90)],
        'Europe PMC': [random.randint(60, 120) for _ in range(90)],
        'Clinical Trials': [random.randint(10, 40) for _ in range(90)]
    })

    # Crear gráfico de líneas con Altair
    chart = alt.Chart(
        chart_data.melt('fecha', var_name='fuente', value_name='publicaciones')
    ).mark_line().encode(
        x=alt.X('fecha:T', title='Fecha'),
        y=alt.Y('publicaciones:Q', title='Número de Publicaciones'),
        color=alt.Color('fuente:N', legend=alt.Legend(title="Fuente")),
        tooltip=['fecha', 'fuente', 'publicaciones']
    ).properties(height=300).interactive()
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
        # ... segunda tarjeta ...
    with col2:
        # ... tarjetas de la columna derecha ...
        pass


# 2. BÚSQUEDA
elif "🔍 Búsqueda Científica" in menu:
    st.title("🔍 Búsqueda Científica Inteligente")

    # Introducción a la herramienta
    st.markdown(
        """
        <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
            <h4 style='margin-top:0'>Búsqueda unificada en las principales bases de datos científicas</h4>
            <p>Nuestra tecnología permite búsquedas simultáneas en PubMed, Europe PMC y otras fuentes científicas con análisis de IA integrado.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Formulario de búsqueda mejorado
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "🔎 Escriba su término de búsqueda",
            value="semaglutide",
            placeholder="Ej: semaglutide in obesity, machine learning diagnostics..."
        )
    with col2:
        max_resultados = st.slider("Resultados por fuente", 5, 50, 10)

    # Opciones avanzadas
    with st.expander("Opciones avanzadas de búsqueda"):
        col1, col2, col3 = st.columns(3)
        with col1:
            idioma = st.selectbox(
                "Idioma", ["Todos", "Inglés", "Español", "Francés", "Alemán"]
            )
            ordenar_por = st.selectbox(
                "Ordenar por", ["Relevancia", "Fecha (reciente)", "Fecha (antigua)", "Factor de impacto"]
            )
        with col2:
            tipo_documento = st.multiselect(
                "Tipo de documento",
                ["Todos", "Artículo original", "Revisión", "Metaanálisis", "Ensayo clínico", "Guía clínica"],
                default=["Todos"]
            )
            años = st.slider("Rango de años", 2000, 2025, (2020, 2025))
        with col3:
            solo_humanos = st.checkbox("Solo estudios en humanos", value=True)
            solo_abiertos = st.checkbox("Solo acceso abierto", value=False)
            incluir_preprints = st.checkbox("Incluir preprints", value=True)

    # Botón de búsqueda principal
    if st.button("Buscar evidencia científica", use_container_width=True):
        # Progress bar
        progress_container = st.empty()
        progress_bar = progress_container.progress(0)
        for i in range(101):
            time.sleep(0.01)
            progress_bar.progress(i)
        progress_container.empty()

        st.success(f"Se encontraron 87 resultados para '{query}' en todas las fuentes")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📑 Todos los resultados", "📊 PubMed", "🌍 Europe PMC", "💡 Análisis de IA"]
        )

        # Todos los resultados
        with tab1:
            for i in range(1, 6):
                with st.expander(f"Efficacy and safety of semaglutide in type 2 diabetes patients - Phase {i} clinical trial"):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"""
                        **Autores:** Jensen AB, Smith JR, Anderson P, et al.

                        **Publicado en:** New England Journal of Medicine • {2025 - i} • Factor de impacto: {round(10.5 - i * 0.5, 1)}

                        **Resumen:** This randomized clinical trial evaluated the efficacy and safety of semaglutide in patients with type 2 diabetes over a 52-week period. The study demonstrated significant improvements in glycemic control and weight reduction compared to placebo, with a favorable safety profile.

                        **Conclusiones clave:** Semaglutide mostró reducciones dependientes de dosis en HbA1c y peso corporal con tolerabilidad aceptable.
                        """)
                        st.markdown("""
                        <div style='display:flex; gap:5px'>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Diabetes</span>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Semaglutide</span>
                            <span style='background-color:#e1f5fe; color:#0277bd; padding:3px 8px; border-radius:15px; font-size:12px'>Clinical Trial</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        **PMID:** 3652891{i}

                        **Citado:** {120 - i * 15} veces

                        **Acceso:** {'Abierto ✓' if i % 2 == 0 else 'Restringido'}
                        """)
                        st.download_button(
                            label="PDF",
                            data=b"sample",
                            file_name=f"semaglutide_study_{i}.pdf",
                            mime="application/pdf"
                        )

        # PubMed
        with tab2:
            if query:
                with st.spinner("Consultando PubMed..."):
                    resultados_pubmed = buscar_pubmed(query, max_resultados)
                if resultados_pubmed:
                    for r in resultados_pubmed:
                        with st.expander(r["Título"]):
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"**Autores:** {r['Autores']}")
                                st.markdown(f"**Fuente:** {r['Fuente']}")
                                st.markdown(f"**Resumen original:**\n\n{r['Resumen']}")
                            with c2:
                                st.markdown(f"**PMID:** {r['PMID']}")
                                st.button("⭐ Guardar", key=f"save_pubmed_{r['PMID']}")
                                st.button("📤 Exportar", key=f"export_pubmed_{r['PMID']}")
                            st.markdown("**🧠 Análisis de IA:**")
                            with st.spinner("Analizando contenido..."):
                                resumen_ia = resumir_texto(r["Resumen"])
                                st.info(resumen_ia)
                else:
                    st.warning("No se encontraron resultados en PubMed.")

        # Europe PMC
        with tab3:
            if query:
                with st.spinner("Consultando Europe PMC..."):
                    resultados_epmc = buscar_europe_pmc(query, max_resultados)
                if resultados_epmc:
                    for e in resultados_epmc:
                        with st.expander(e["Título"]):
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"**Fuente:** {e['Fuente']}")
                                st.markdown(f"**Tipo de publicación:** {e['Tipo']}")
                                st.markdown(f"**Enlace:** [Ver artículo completo]({e['Enlace']})")
                            with c2:
                                st.markdown(f"**ID:** {e['ID']}")
                                st.button("⭐ Guardar", key=f"save_epmc_{e['ID']}")
                                st.button("📤 Exportar", key=f"export_epmc_{e['ID']}")
                else:
                    st.warning("No se encontraron resultados en Europe PMC.")

        # IA
        with tab4:
            st.subheader("🧠 Análisis de tendencias por IA")
            st.markdown(
                """
                <div style='background-color:#f0f7ff; padding:20px; border-radius:5px; margin-bottom:20px;'>
                    <h4 style='margin-top:0'>Insights sobre semaglutide</h4>
                    <p>Basado en el análisis de 87 publicaciones recientes, encontramos las siguientes tendencias:</p>
                    <ul>
                        <li><strong>Efectividad:</strong> El 92% de los estudios reportan efectividad significativa en reducción de peso y control glucémico.</li>
                        <li><strong>Poblaciones:</strong> Predominio en América del Norte y Europa, con creciente interés en diversidad étnica.</li>
                        <li><strong>Efectos secundarios:</strong> Gastrointestinales, con tendencia a disminuir tras las primeras semanas.</li>
                        <li><strong>Comparaciones:</strong> Superioridad frente a otros GLP-1 RA en reducción de HbA1c y peso.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

# 3. CLINICAL TRIALS
elif "🧪 Clinical Trials" in menu:
    st.title("🧪 Monitoreo de Ensayos Clínicos")

    st.markdown(
        """
        <div style='background-color:#f0f7ff; padding:15px; border-radius:5px; margin-bottom:20px;'>
            <h4 style='margin-top:0'>Seguimiento en tiempo real de ensayos clínicos globales</h4>
            <p>Monitoree los ensayos clínicos más relevantes, sus actualizaciones y resultados preliminares en todo el mundo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filtros
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

    query_trials = st.text_input(
        "🔎 Buscar ensayos clínicos",
        placeholder="Ej: semaglutide, cáncer de páncreas, hipertensión resistente..."
    )

    if st.button("Buscar ensayos clínicos", use_container_width=True):
        st.success("Se encontraron 42 ensayos clínicos que coinciden con sus criterios")

        for i in range(1, 6):
            with st.expander(f"SEMAGOLD-{i}: Evaluación de semaglutide oral en pacientes con DMT2 y enfermedad cardiovascular"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"""
                    **ID:** NCT0{random.randint(1000000, 9999999)}

                    **Patrocinador:** {'Industria Farmacéutica' if i % 2 == 0 else 'Centro Médico Universitario'}

                    **Fase:** {random.choice(['II', 'III', 'IV'])}

                    **Estado:** {random.choice(['Reclutando', 'Activo, no reclutando'])}

                    **Sitios activos:** {random.randint(10, 50)} en {random.randint(3, 15)} países

                    **Intervención principal:** Semaglutide oral {random.choice(['10mg', '15mg', '20mg'])} una vez al día vs placebo

                    **Actualización reciente:** {random.choice(['Resultados preliminares', 'Cambio en criterios de inclusión', 'Nuevo sitio de estudio', 'Reporte de seguridad'])}
                    """)
                with c2:
                    st.markdown(f"""
                    **Participantes:** {random.randint(1000, 5000)}

                    **Fecha inicio:** {random.choice(['Ene', 'Feb', 'Mar', 'Abr'])} 202{random.randint(3, 5)}

                    **Fecha estimada conclusión:** {random.choice(['Jun', 'Jul', 'Ago', 'Sep', 'Oct'])} 202{random.randint(5, 7)}
                    """)
                    st.button("📌 Seguir", key=f"follow_trial_{i}")
                    st.button("📑 Protocolo", key=f"protocol_trial_{i}")

                st.markdown("##### Criterios de inclusión principales:")
                st.markdown(
                    """
                    - Pacientes adultos (>18 años)
                    - Diabetes mellitus tipo 2 diagnosticada
                    - HbA1c entre 7.0% y 10.5%
                    - Enfermedad cardiovascular aterosclerótica establecida
                    - IMC ≥25 kg/m²
                    """
                )

                st.markdown("##### Distribución de sitios de estudio:")
                trial_sites = pd.DataFrame({
                    'lat': [random.uniform(25, 60) for _ in range(15)],
                    'lon': [random.uniform(-120, 30) for _ in range(15)],
                    'sitio': [f'Centro {random.randint(1, 100)}' for _ in range(15)],
                    'pacientes_reclutados': [random.randint(10, 100) for _ in range(15)]
                })
                st.map(trial_sites)

        st.markdown("##### Línea de tiempo del ensayo:")
        timeline_chart = alt.Chart(pd.DataFrame({
            'Fase': ['Diseño', 'Inicio', 'Reclutamiento', 'Tratamiento', 'Análisis', 'Resultados'],
            'Inicio': [0, 3, 6, 8, 24, 30],
            'Fin':    [3, 6, 18, 24, 30, 36],
            'Estado': ['Completado', 'Completado', 'En progreso', 'Planificado', 'Planificado', 'Planificado']
        })).mark_bar().encode(
            x='Inicio', x2='Fin', y='Fase',
            color=alt.Color('Estado', scale=alt.Scale(
                domain=['Completado','En progreso','Planificado'],
                range=['#2ecc71','#3498db','#95a5a6']
            ))
        ).properties(height=200)
        st.altair_chart(timeline_chart, use_container_width=True)

        st.markdown("##### Resultados preliminares disponibles:")
        results_data = pd.DataFrame({
            'Grupo': ['Semaglutide','Placebo'],
            'Reducción HbA1c (%)': [1.4 + random.uniform(-0.2,0.2), 0.3 + random.uniform(-0.1,0.1)],
            'Reducción peso (kg)': [4.5 + random.uniform(-0.5,0.5), 0.8 + random.uniform(-0.2,0.2)],
            'Eventos CV (%)': [3.2 + random.uniform(-0.5,0.5), 5.1 + random.uniform(-0.5,0.5)]
        })
        st.dataframe(results_data, use_container_width=True)
        st.info("💡 **Análisis IA:** Los datos preliminares sugieren eficacia significativa en HbA1c y peso comparado con placebo.")

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

    # --- Análisis Comparativo ---
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

        endpoints = st.multiselect(
            "Endpoints a comparar",
            ["Reducción HbA1c", "Pérdida de peso", "Eventos cardiovasculares", "Eventos adversos", "Abandonos"],
            default=["Reducción HbA1c", "Pérdida de peso"]
        )

        if st.button("Ejecutar análisis comparativo", use_container_width=True):
            st.success(f"Analizando diferencias entre {tratamiento1} y {tratamiento2} usando 17 estudios")

            # Forest plot simulado
            st.subheader("Forest Plot - Diferencia media en reducción de HbA1c")
            forest_data = pd.DataFrame({
                'Estudio': [f"Estudio {chr(65 + i)}" for i in range(8)],
                'MeanDiff': [-0.3, -0.5, -0.2, -0.4, -0.6, -0.3, -0.5, -0.4],
                'LowerCI': [-0.5, -0.7, -0.4, -0.6, -0.8, -0.5, -0.7, -0.6],
                'UpperCI': [-0.1, -0.3, -0.1, -0.2, -0.4, -0.1, -0.3, -0.2]
            })
            base = alt.Chart(forest_data).encode(y=alt.Y('Estudio:N', sort=None))
            lines = base.mark_rule().encode(
                x=alt.X('LowerCI:Q', title='Diferencia en HbA1c (%)'),
                x2='UpperCI:Q'
            )
            points = base.mark_circle(size=100).encode(
                x='MeanDiff:Q',
                tooltip=['Estudio','MeanDiff','LowerCI','UpperCI']
            )
            st.altair_chart((lines + points).properties(height=300), use_container_width=True)

            # Gráfico de comparación de barras
            st.subheader("Comparación de endpoints")
            comp_df = pd.DataFrame({
                'Endpoint': ['HbA1c (%)', 'Peso (kg)', 'PAS (mmHg)', 'Eventos CV (%)'],
                tratamiento1: [1.6, 5.2, 3.8, 3.2],
                tratamiento2: [1.2, 3.6, 2.9, 3.5],
            }).melt('Endpoint', var_name='Tratamiento', value_name='Valor')
            bar = alt.Chart(comp_df).mark_bar().encode(
                x='Tratamiento:N',
                y='Valor:Q',
                color='Tratamiento:N',
                column='Endpoint:N',
                tooltip=['Valor']
            ).properties(width=150)
            st.altair_chart(bar, use_container_width=True)

    # --- Meta-análisis ---
    elif tipo_analisis == "Meta-análisis":
        st.subheader("Generador de Meta-análisis")

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

        if st.button("Ejecutar meta-análisis", use_container_width=True):
            st.success("Meta-análisis completado – 23 estudios incluidos")
            st.image("https://via.placeholder.com/700x400?text=Forest+Plot", use_column_width=True)

    # --- Tendencias temporales ---
    elif tipo_analisis == "Tendencias temporales":
        st.subheader("Análisis de Tendencias Temporales")

        col1, col2 = st.columns(2)
        with col1:
            area_inv = st.selectbox(
                "Área de investigación",
                ["Diabetes", "Oncología", "Cardiología", "Neurología", "Inmunología"]
            )
        with col2:
            periodo = st.slider("Periodo", 2000, 2025, (2010, 2025))

        temas = st.multiselect(
            "Temas",
            ["GLP-1", "SGLT2", "Inmunoterapia", "Inteligencia Artificial", "Terapia génica", "Medicina de precisión"],
            default=["GLP-1", "SGLT2"]
        )

        if st.button("Analizar tendencias", use_container_width=True):
            years = list(range(periodo[0], periodo[1] + 1))
            df = pd.DataFrame({
                'Año': years * len(temas),
                'Tema': sum([[t]*len(years) for t in temas], []),
                'Publicaciones': [random.randint(50, 200) for _ in range(len(years) * len(temas))]
            })
            trend = alt.Chart(df).mark_line(point=True).encode(
                x='Año:O',
                y='Publicaciones:Q',
                color='Tema:N',
                tooltip=['Año','Publicaciones']
            ).properties(height=300)
            st.altair_chart(trend, use_container_width=True)

    # --- Network Analysis ---
    elif tipo_analisis == "Network Analysis":
        st.subheader("Network Analysis de Evidencia Científica")

        col1, col2 = st.columns(2)
        with col1:
            concepto = st.selectbox(
                "Concepto central",
                ["Diabetes tipo 2", "Alzheimer", "Cáncer de páncreas", "Obesidad", "COVID-19"]
            )
        with col2:
            profundidad = st.slider("Profundidad de red", 1, 4, 2)
        tipo_red = st.radio(
            "Tipo de red",
            ["Conceptos relacionados", "Co-citación de autores", "Colaboración institucional"],
            horizontal=True
        )

        if st.button("Generar red", use_container_width=True):
            st.success(f"Red generada para {concepto}")
            st.image("https://via.placeholder.com/800x500?text=Network+Analysis", use_column_width=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Nodos", "284")
            m2.metric("Conexiones", "1,240")
            m3.metric("Centralidad", "3.2")
            m4.metric("Densidad", "0.042")


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
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔔 Alertas", "🏷️ Etiquetas", "🔍 Búsqueda", "🔐 Cuenta"])

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
                st.markdown("&nbsp;")
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
                st.markdown(f"Relevancia: {'🟢' * tema['relevancia']}{'⚪' * (5 - tema['relevancia'])}")

            with col3:
                st.markdown(f"{tema['frecuencia']} ✏️ 🗑️")

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
        st.markdown(
            f"""
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
        condicion = st.selectbox("Condición", [
            "Contiene en título",
            "Contiene en abstract",
            "Autor es",
            "Journal es",
            "Factor de impacto >"])
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
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; padding:8px; background-color:#f8f9fa; border-radius:5px; margin-bottom:5px;">
            <div><strong>Si</strong> [{regla['condicion']}] <strong>es</strong> \"{regla['valor']}\"</div>
            <div><strong>→ Aplicar</strong> \"{regla['etiqueta']}\"</div>
            <div>✏️ 🗑️</div>
        </div>
        """, unsafe_allow_html=True)

# Guardar configuración
st.button("💾 Guardar configuración de etiquetas", use_container_width=True)

# Añadir acción para mostrar información sobre la aplicación
def show_acerca_de():
    st.sidebar.markdown("""
    **EvidenceWatch Pro v2.5**

    Desarrollado por MedTech Solutions

    Esta aplicación está diseñada para profesionales de la salud que desean mantenerse actualizados con la última evidencia científica relevante para su práctica clínica.

    © 2025 Todos los derechos reservados
    """)

with st.sidebar:
    st.markdown("---")
    if st.button("ℹ️ Acerca de EvidenceWatch"):
        show_acerca_de()
