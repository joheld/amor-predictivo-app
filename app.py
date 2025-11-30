import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="Love Algorithm v2.0 Pro",
    layout="wide",
    page_icon="❤️"
)

TITLE = "LOVE ALGORITHM v2.0 PRO"

# ========== CSS PERSONALIZADO ESTILO DARK MODE BI ==========
st.markdown("""
<style>
    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #FF4B4B;
    }
    h1, h2, h3 {
        font-family: Helvetica Neue, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ========== STATE MANAGEMENT ==========
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {"user": {}, "candidate": {}, "missions": {}}

# ========== MOTOR DE CÁLCULO: EL CEREBRO ==========
def calculate_deep_metrics(data):
    """
    Motor de reglas deterministas que simula un análisis experto.
    Retorna un diccionario con scores desglosados y explicaciones.
    """
    u = data["user"]
    c = data["candidate"]
    m = data["missions"]
    
    base_score = 50
    log = []
    
    # ========== 1. SCORE BASE: Compatibilidad Teórica ==========
    
    # ========== A. Análisis Evolutivo: Edad y Fertilidad vs Objetivo ==========
    evo_score = 0
    if u.get("goal") == "Familia e Hijos":
        if 20 <= c.get("age", 0) <= 32:
            evo_score = 20
            log.append("✅ Ventana Fértil Óptima: La edad 20-32 maximiza probabilidad de embarazo saludable.")
        elif 33 <= c.get("age", 0) <= 37:
            evo_score = 10
            log.append("⚠️ Ventana Fértil Media: Edad 32 implica urgencia biológica moderada.")
        else:
            evo_score = -10
            log.append("❌ Riesgo Obstétrico: Edad fuera de rango óptimo para familia numerosa.")
    
    # ========== B. Análisis Gottman: Misiones de Campo ==========
    gottman_score = 0
    if m.get("testno") == "Aceptacin tranquila":
        gottman_score = 25
        log.append("✅ Bajo Conflicto: Aceptar un No indica seguridad emocional y ausencia de rasgos controladores.")
    elif m.get("testno") == "Molestia visible":
        gottman_score = -15
        log.append("⚠️ Alerta de Neuroticismo: La molestia ante límites sugiere baja tolerancia a la frustración.")
    else:
        gottman_score = -40
        log.append("❌ RED FLAG Narcisismo: La manipulación/venganza ante un límite es predictor #1 de abuso emocional.")
    
    # ========== C. Análisis Cognitivo: Big 5 - Openness ==========
    cog_score = 0
    if m.get("testmono") == "Pregunt con inters":
        cog_score = 25
        log.append("✅ Compatibilidad Intelectual: Interés activo (Active Constructive Responding) predice longevidad.")
    elif m.get("testmono") == "Escuch pasivamente":
        cog_score = 5
        log.append("⚠️ Riesgo de Aburrimiento: Escucha pasiva es aceptable, pero tú necesitas estimulación intelectual.")
    else:
        cog_score = -30
        log.append("❌ Desprecio Intelectual: Ignorar tu pasión es un Jinete del Apocalipsis (Gottman).")
    
    # ========== D. Análisis de Madurez: Responsabilidad Radical ==========
    mat_score = 0
    if len(m.get("testex", "")) >= 10 and ("culpa" not in m.get("testex", "").lower() or "mi error" in m.get("testex", "").lower()):
        mat_score = 15
        log.append("✅ Locus de Control Interno: Asumir errores propios indica madurez psicológica para resolver conflictos.")
    else:
        mat_score = -20
        log.append("❌ Victimización: No articular autocrítica sugiere inmadurez emocional.")
    
    # ========== TOTALES ==========
    final_score = base_score + evo_score + gottman_score + cog_score + mat_score
    final_score = max(0, min(100, final_score))
    
    return {
        "total": final_score,
        "breakdown": {
            "Biología/Evolutiva": evo_score,
            "Dinámica de Conflicto (Gottman)": gottman_score,
            "Intelecto/Openness": cog_score,
            "Madurez Emocional": mat_score,
        },
        "reasons": log
    }

# ========== UI: DASHBOARD ==========
def render_dashboard(results):
    st.divider()
    st.markdown("## Dashboard Analítico de Viabilidad Relacional")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### Índice de Éxito (5 Años)")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=results["total"],
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "white"},
                "steps": [
                    {"range": [0, 40], "color": "#FF4B4B"},
                    {"range": [40, 70], "color": "#FFA500"},
                    {"range": [70, 100], "color": "#00CC96"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": 70
                }
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        veredicto = "✅ PROCEDER" if results["total"] >= 70 else ("⚠️ PRECAUCIÓN" if results["total"] >= 40 else "❌ ABORTAR")
        st.metric("Veredicto Algortímico", veredicto)
    
    with col2:
        st.markdown("### Desglose de Impacto por Dimensión")
        df_breakdown = pd.DataFrame(list(results["breakdown"].items()), columns=["Dimensión", "Puntos"])
        fig_bar = px.bar(df_breakdown, x="Puntos", y="Dimensión", orientation="h", 
                         color="Puntos", color_continuous_scale="RdYlGn", text="Puntos")
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col3:
        st.markdown("### Datos del Sujeto")
        st.metric("Edad Candidata", st.session_state.data["candidate"].get("age", "N/A"))
        st.metric("Ingreso Usuario", f"${st.session_state.data['user'].get('income', 'N/A')}")
        st.metric("Objetivo", "Familia")
    
    st.subheader("Interpretación Detallada de Factores")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Fortalezas Detectadas**")
        for reason in results["reasons"]:
            if "✅" in reason:
                st.info(reason)
    with c2:
        st.markdown("**Riesgos y Amenazas**")
        risk_found = False
        for reason in results["reasons"]:
            if "❌" in reason or "⚠️" in reason:
                risk_found = True
                st.error(reason)
        if not risk_found:
            st.success("No se detectaron riesgos críticos en las pruebas realizadas.")
    
    st.subheader("Plan de Acción Sugerido")
    if results["total"] >= 70:
        st.markdown("**Próximo paso:** Iniciar conversaciones sobre finanzas y logística de vivienda. Mantener el nivel de comunicación intelectual.")
    elif results["total"] >= 40:
        st.markdown("**Próximo paso:** Distanciamiento estratégico. Justificación: La incompatibilidad en resolución de conflictos (Test del No) garantiza una relación tóxica a mediano plazo.")
    else:
        st.markdown("**Próximo paso:** Extender período de prueba 3 meses más. Dato faltante: Se requiere observar reacción bajo estrés financiero real.")

# ========== LÓGICA DE PASOS (WIZARD) ==========
def main():
    st.title(TITLE)
    
    st.sidebar.title("Progreso")
    st.sidebar.progress(st.session_state.step / 4)
    
    if st.sidebar.button("🔄 Reiniciar Sistema"):
        st.session_state.step = 1
        st.rerun()
    
    # ========== PASO 1: CALIBRACIÓN USUARIO ==========
    if st.session_state.step == 1:
        st.markdown("## Fase 1: Calibración del Operador")
        with st.form("step1"):
            age = st.number_input("Tu Edad", 20, 60, 30)
            income = st.number_input("Ingreso Mensual (USD)", 0, 10000, 2400)
            goal = st.selectbox("Objetivo", ["Familia e Hijos", "Pareja Estable", "Casual"])
            if st.form_submit_button("➡️ Siguiente"):
                st.session_state.data["user"] = {"age": age, "income": income, "goal": goal}
                st.session_state.step = 2
                st.rerun()
    
    # ========== PASO 2: PERFIL CANDIDATA ==========
    elif st.session_state.step == 2:
        st.markdown("## Fase 2: Datos del Sujeto")
        with st.form("step2"):
            name = st.text_input("Nombre")
            age_c = st.number_input("Edad de ella", 18, 50, 28)
            kids = st.checkbox("¿Tiene hijos?")
            if st.form_submit_button("➡️ Siguiente"):
                st.session_state.data["candidate"] = {"name": name, "age": age_c, "has_kids": kids}
                st.session_state.step = 3
                st.rerun()
    
    # ========== PASO 3: RESULTADOS DE MISIONES ==========
    elif st.session_state.step == 3:
        st.markdown("## Fase 3: Input de Operaciones de Campo")
        st.info("Introduce los resultados de los experimentos conductuales.")
        with st.form("step3"):
            st.markdown("**1. Reacción al Límite (Test del No)**")
            rno = st.radio("Resultado", ["Aceptacin tranquila", "Molestia visible", "ManipulaciónVenganza"])
            
            st.markdown("**2. Reacción Intelectual**")
            rmono = st.radio("Resultado", ["Pregunt con inters", "Escuch pasivamente", "IgnorCelular"])
            
            st.markdown("**3. Madurez (Pregunta del Ex)**")
            rex = st.text_area("¿Qué dijo sobre su error pasado?", "Admitió que era inmadura...")
            
            if st.form_submit_button("📊 GENERAR DASHBOARD"):
                st.session_state.data["missions"] = {"testno": rno, "testmono": rmono, "testex": rex}
                st.session_state.step = 4
                st.rerun()
    
    # ========== PASO 4: DASHBOARD FINAL ==========
    elif st.session_state.step == 4:
        results = calculate_deep_metrics(st.session_state.data)
        render_dashboard(results)

if __name__ == "__main__":
    main()
