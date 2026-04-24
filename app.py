# --- 1. PANTALLA INICIAL (REDISEÑO TÉCNICO) ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ CIFRADO HILL: PROTOCOLO TÉCNICO</h1>", unsafe_allow_html=True)
    
    # Caja de cristal para el concepto core
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color:#4ADE80; margin-bottom:10px;'>Cifrado Poligráfico de Lester S. Hill</h3>
        <p style='color:#E0E1DD; font-size:16px;'>
            Este sistema utiliza <b>Álgebra Lineal</b> para transformar bloques de texto en datos encriptados mediante una transformación lineal sobre el anillo <b>Z₂₆</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # El flujo de trabajo en 3 pasos directos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border-left: 3px solid #778DA9; padding-left:15px;'>
            <small style='color:#778DA9;'>FASE 01</small>
            <h4 style='margin:0;'>Vectorización</h4>
            <p style='font-size:12px;'>Mapeo de caracteres a valores numéricos (A=0 ... Z=25).</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='border-left: 3px solid #778DA9; padding-left:15px;'>
            <small style='color:#778DA9;'>FASE 02</small>
            <h4 style='margin:0;'>Cifrado</h4>
            <p style='font-size:12px;'>Multiplicación matricial: <b>C = K · P (mod 26)</b>.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='border-left: 3px solid #778DA9; padding-left:15px;'>
            <small style='color:#778DA9;'>FASE 03</small>
            <h4 style='margin:0;'>Validación</h4>
            <p style='font-size:12px;'>La matriz <b>K</b> debe ser invertible para permitir el descifrado.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Matriz centrada y estilizada
    st.markdown("<div style='text-align:center;'><p style='color:#778DA9; margin-bottom:0;'>Matriz Clave de la Sesión:</p></div>", unsafe_allow_html=True)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    # Botón de acción
    if st.button("🚀 INICIAR EVALUACIÓN"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()
