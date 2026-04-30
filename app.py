# --- 1. PANTALLA INICIAL (ACTUALIZADA) ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ CIFRADO HILL: PROTOCOLO TÉCNICO</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color:#4ADE80; margin-bottom:15px; text-align:center;'>Explicación del Sistema</h3>
        <p style='text-align:justify; color:#E0E1DD; line-height:1.6;'>
            ¡Bienvenidos al desafío de Criptografía! Este sistema es un <b>Banco de Preguntas</b> diseñado para evaluar tus conocimientos sobre el método de cifrado Hill. 
            La prueba consta de <b>10 preguntas</b> seleccionadas de forma aleatoria. Para superar el reto y ganar la prueba, deberás acertar al menos <b>6 respuestas</b>; de lo contrario, el sistema marcará el estado como reprobado.
        </p>
        
        <div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border-left: 5px solid #778DA9; text-align:left;'>
            <h4 style='color:#778DA9; margin-top:0;'>📌 Fundamentos del Método</h4>
            <ul style='color:#BDC3C7; font-size:14px;'>
                <li><b>Alfabeto Numérico:</b> El sistema opera en un espacio vectorial donde las letras se asignan de <b>A=0</b> hasta <b>Z=25</b>.</li>
                <li><b>Operaciones:</b> Todo el procesamiento se basa en multiplicación de matrices y aritmética modular (módulo 26).</li>
                <li><b>Seguridad:</b> La clave utilizada debe ser una matriz invertible para garantizar la integridad del mensaje.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualización de la Matriz de la sesión
    st.markdown("<p style='text-align:center; color:#778DA9; margin-bottom:0;'>Matriz Clave Activa para Cálculos:</p>", unsafe_allow_html=True)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 INICIAR EVALUACIÓN"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()
