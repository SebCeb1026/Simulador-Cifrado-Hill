# --- 1. PANTALLA INICIAL MEJORADA ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ SISTEMA DE CIFRADO HILL</h1>", unsafe_allow_html=True)
    
    # Contenedor principal con efecto cristal
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color:#E0E1DD; margin-bottom:20px;'>🛠️ Protocolo de Operación</h2>
        <p style='color:#778DA9;'>Sigue estos 3 pasos para procesar la información:</p>
    </div>
    """, unsafe_allow_html=True)

    # Columnas para explicar el proceso visualmente
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align:center; background:rgba(255,255,255,0.05); padding:15px; border-radius:15px;'>
            <h1 style='margin:0;'>🔡</h1>
            <b style='color:#4ADE80;'>1. TRADUCIR</b>
            <p style='font-size:12px;'>Convertimos letras a números según su posición (A=0, B=1...)</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='text-align:center; background:rgba(255,255,255,0.05); padding:15px; border-radius:15px;'>
            <h1 style='margin:0;'>✖️</h1>
            <b style='color:#4ADE80;'>2. OPERAR</b>
            <p style='font-size:12px;'>Multiplicamos el vector del mensaje por nuestra matriz clave.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='text-align:center; background:rgba(255,255,255,0.05); padding:15px; border-radius:15px;'>
            <h1 style='margin:0;'>🔢</h1>
            <b style='color:#4ADE80;'>3. AJUSTAR</b>
            <p style='font-size:12px;'>Aplicamos Módulo 26 para que el resultado sea una letra válida.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mostrar la matriz de forma elegante
    st.markdown("<p style='text-align:center; color:#778DA9;'>Matriz de Encriptación Activa:</p>", unsafe_allow_html=True)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    if st.button("🚀 INICIAR DESAFÍO"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()
