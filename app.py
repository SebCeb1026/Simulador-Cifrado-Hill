import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz", layout="centered")

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

# --- PREGUNTAS SIMPLIFICADAS ---
def obtener_quiz():
    return [
        {"p": "¿En qué año se creó oficialmente este sistema de cifrado?", "o": ["1929", "1945", "1914", "1935"], "c": "1929"},
        {"p": "Si usas la clave de nuestro proyecto, ¿cuál es el resultado de cifrar 'MA'?", "o": ["KY", "AT", "RI", "ZE"], "c": "KY"},
        {"p": "¿Cómo se llama el método matemático que usa el 'residuo' de una división?", "o": ["Aritmética Modular", "Cálculo Integral", "Álgebra de Boole", "Trigonometría"], "c": "Aritmética Modular"},
        {"p": "Si el cálculo final te da 36, ¿qué número queda tras aplicar el Módulo 26?", "o": ["10", "15", "5", "0"], "c": "10"},
        {"p": "¿Qué herramienta del Álgebra Lineal es la 'llave' en este cifrado?", "o": ["Las Matrices", "Las Derivadas", "Los Vectores Propios", "Las Integrales"], "c": "Las Matrices"},
        {"p": "En nuestra tabla de conversión, ¿qué número le asignamos a la letra 'A'?", "o": ["0", "1", "26", "A"], "c": "0"},
        {"p": "Si contamos A=0, B=1, C=2... ¿Qué número le toca a la letra 'D'?", "o": ["3", "4", "2", "5"], "c": "3"},
        {"p": "¿Cuál es el objetivo principal de este trabajo?", "o": ["Protección de mensajes", "Diseño de puentes", "Contabilidad", "Creación de música"], "c": "Protección de mensajes"},
        {"p": "Si una operación da 10, ¿qué letra buscamos en la tabla?", "o": ["K", "A", "Z", "M"], "c": "K"},
        {"p": "En la matriz de nuestro ejercicio, ¿cuál es el último número (abajo a la derecha)?", "o": ["5", "3", "2", "0"], "c": "5"}
    ]

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = obtener_quiz()

# --- PANTALLA 1: EXPLICACIÓN ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🔵 Cifrado Hill: Guía del Reto</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 📂 ¿Qué necesitas saber?
    Para ganar este reto, recuerda estos 3 puntos clave de nuestra exposición:
    
    1. **Los Números:** Cada letra es un número del **0 al 25** (A es 0).
    2. **La Clave:** Usamos una **Matriz** para transformar las palabras.
    3. **El Residuo:** Si un número se pasa de 26, usamos lo que sobra (Módulo 26).
    
    *¡Suerte! Demuestra lo que aprendiste hoy.*
    """)
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
    
    st.markdown(f"""
    <div class='question-box'>
        <h3 style='text-align:center; margin:0; line-height: 1.4;'>{actual['p']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    opciones_mezcladas = st.session_state[f"opciones_{st.session_state.indice}"]
    cols = st.columns(2)
    for i, opc in enumerate(opciones_mezcladas):
        with cols[i % 2]:
            if st.button(opc):
                if opc == actual["c"]:
                    st.success("¡Correcto! 💎")
                    st.session_state.buenas += 1
                else:
                    st.error(f"Incorrecto ❌")
                    st.session_state.malas += 1
                time.sleep(0.8)
                if st.session_state.indice < 9:
                    st.session_state.indice += 1
                else:
                    st.session_state.terminado = True
                st.rerun()

# --- PANTALLA 3: RESUMEN FINAL ---
else:
    st.balloons()
    st.markdown("<h1 class='main-title'>🏁 ¡Fin del Reto!</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#1B4332; text-align:center;'><h3>Buenas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#641212; text-align:center;'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center; margin-top:20px;'>Tu Puntaje: {total} / 100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Volver a Intentar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
