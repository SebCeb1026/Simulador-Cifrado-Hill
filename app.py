# --- 1. PANTALLA INICIAL (VERSIÓN TÉCNICA AVANZADA) ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ PROTOCOLO DE CIFRADO HILL</h1>", unsafe_allow_html=True)
    
    # Contenedor principal con efecto cristal y descripción técnica
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color:#4ADE80; margin-bottom:15px; text-align:left;'>📊 Análisis de Algoritmo</h3>
        <p style='color:#E0E1DD; font-size:16px; line-height:1.6; text-align:justify;'>
            El Cifrado Hill es un sistema de sustitución <b>poligráfico</b> basado en el álgebra de matrices. 
            A diferencia de los métodos clásicos, este algoritmo procesa el texto en bloques de <i>n</i> dimensiones, 
            lo que permite ocultar las estadísticas del lenguaje mediante una <b>transformación lineal</b> sobre el espacio <b>Z₂₆</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Rejilla de especificaciones técnicas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); padding:15px; border-radius:15px; border-top: 3px solid #778DA9;'>
            <h5 style='margin:0; color:#4ADE80;'>VECTORIZACIÓN</h5>
            <p style='font-size:12px; color:#BDC3C7;'>Conversión de grafemas en valores numéricos dentro del anillo decimal 26.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); padding:15px; border-radius:15px; border-top: 3px solid #778DA9;'>
            <h5 style='margin:0; color:#4ADE80;'>PROCESAMIENTO</h5>
            <p style='font-size:12px; color:#BDC3C7;'>Producto matricial: <b>C ≡ K · P (mod 26)</b> para la generación del criptograma.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); padding:15px; border-radius:15px; border-top: 3px solid #778DA9;'>
            <h5 style='margin:0; color:#4ADE80;'>REQUISITO</h5>
            <p style='font-size:12px; color:#BDC3C7;'>La clave <b>K</b> debe poseer determinante coprimo con 26 para asegurar su inversión.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualización de la Matriz de Seguridad
    st.markdown("""
    <div style='text-align:center;'>
        <p style='color:#778DA9; font-size:13px; text-transform:uppercase; letter-spacing:3px;'>Matriz Clave Activa</p>
    """, unsafe_allow_html=True)
    
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    st.markdown("</div><br>", unsafe_allow_html=True)
    
    if st.button("🚀 INICIAR EVALUACIÓN TÉCNICA"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()
