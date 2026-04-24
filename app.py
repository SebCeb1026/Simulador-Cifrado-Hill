import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz - Pro", layout="centered")

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A; color: #E0E1DD; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        font-weight: bold; background-color: #1B263B;
        color: #778DA9; border: 2px solid #415A77; transition: 0.4s;
    }
    .stButton>button:hover { background-color: #415A77; color: #E0E1DD; border: 2px solid #778DA9; }
    .main-title { text-align: center; color: #E0E1DD; font-weight: 800; margin-bottom: 30px; }
    .question-box { background-color: #1B263B; padding: 25px; border-radius: 15px; border-left: 5px solid #415A77; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN ---
if 'jugando' not in st.session_state:
    st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.buenas = 0
    st.session_state.malas = 0
    st.session_state.terminado = False

# --- PREGUNTAS VARIADAS (Teoría + 3 Ejercicios Reales) ---
def obtener_quiz():
    return [
        {"p": "¿En qué año se creó oficialmente este sistema de cifrado?", "o": ["1929", "1945", "1914", "1935"], "c": "1929"},
        # EJERCICIO 1
        {"p": "📝 RETO: Si vas a cifrar la palabra 'BE' (B=1, E=4) con nuestra matriz, ¿cuál es el primer paso del cálculo?", "o": ["Multiplicar la matriz por el vector (1, 4)", "Dividir 4 entre 26", "Sumar 1 + 4", "Restar la matriz a las letras"], "c": "Multiplicar la matriz por el vector (1, 4)"},
        {"p": "¿Cómo se llama el método que usa el residuo de la división por 26?", "o": ["Aritmética Modular", "Cálculo Integral", "Álgebra de Boole", "Trigonometría"], "c": "Aritmética Modular"},
        # EJERCICIO 2
        {"p": "📝 RETO: Al multiplicar la primera fila [3, 3] por el vector 'MA' (12, 0), el resultado es 36. ¿Qué letra es el resultado final tras aplicar el Módulo 26?", "o": ["K (10)", "Y (24)", "A (0)", "L (11)"], "c": "K (10)"},
        {"p": "¿Qué herramienta matemática es la 'llave' en este cifrado?", "o": ["Las Matrices", "Las Derivadas", "Los Vectores", "Las Integrales"], "c": "Las Matrices"},
        {"p": "En nuestra tabla de conversión, ¿qué número le asignamos a la letra 'A'?", "o": ["0", "1", "26", "A"], "c": "0"},
        # EJERCICIO 3
        {"p": "📝 RETO: Si un compañero calcula un número y le da 53, ¿cuál sería el valor correcto en el sistema Hill (Módulo 26)?", "o": ["1 (porque 53 = 2*26 + 1)", "27", "0", "5"], "c": "1 (porque 53 = 2*26 + 1)"},
        {"p": "¿Cuál es el objetivo principal de este sistema?", "o": ["Protección de mensajes", "Diseño de puentes", "Contabilidad", "Creación de música"], "c": "Protección de mensajes"},
        {"p": "Si una operación da 24, ¿qué letra buscamos en la tabla?", "o": ["Y", "K", "Z", "X"], "c": "Y"},
        {"p": "En nuestra matriz, ¿qué número está en la esquina inferior derecha?", "o": ["5", "3", "2", "0"], "c": "5"}
    ]

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = obtener_quiz()

# --- PANTALLA 1: BIENVENIDA ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🌟 ¡Bienvenidos a los juegos del Cifrado Hill!</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 📂 Repaso para los Retos:
    - **Aritmética:** Si el resultado > 25, divide por 26 y usa el residuo.
    - **Conversión:** A=0, B=1, ..., Z=25.
    - **Nuestra Matriz:**
    """)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    if st.button("Inicio de prueba"):
        st.session_state.jugando = True
        st.rerun()

# --- PANTALLA 2: EL QUIZ ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    
    if f"opciones_{st.session_state.indice}" not in st.session_state:
        ops = actual["o"].copy()
        random.shuffle(ops)
        st.session_state[f"opciones_{st.session_state.indice}"] = ops
    
    st.markdown(f"<p style='text-align:right; color:#778DA9;'>Reto {st.session_state.indice + 1} de 10</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'><h3 style='text-align:center; margin:0;'>{actual['p']}</h3></div>", unsafe_allow_html=True)
    
    opciones_mezcladas = st.session_state[f"opciones_{st.session_state.indice}"]
    cols = st.columns(2)
    for i, opc in enumerate(opciones_mezcladas):
        with cols[i % 2]:
            if st.button(opc):
                if opc == actual["c"]:
                    st.success("¡Correcto! 💎")
                    st.session_state.buenas += 1
                else:
                    st.error("Incorrecto ❌")
                    st.session_state.malas += 1
                time.sleep(0.8)
                if st.session_state.indice < 9: st.session_state.indice += 1
                else: st.session_state.terminado = True
                st.rerun()

# --- PANTALLA 3: FINAL ---
else:
    st.balloons()
    st.markdown("<h1 class='main-title'>🏁 ¡Fin del Desafío!</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#1B4332; text-align:center;'><h3>Buenas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#641212; text-align:center;'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    if st.button("🔄 Volver a Intentar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
