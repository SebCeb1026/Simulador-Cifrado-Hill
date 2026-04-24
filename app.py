import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz - Visual", layout="centered")

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A; color: #E0E1DD; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.8em; 
        font-weight: bold; background-color: #1B263B;
        color: #778DA9; border: 2px solid #415A77; transition: 0.4s;
    }
    .stButton>button:hover { background-color: #415A77; color: #E0E1DD; }
    .main-title { text-align: center; color: #E0E1DD; font-weight: 800; }
    .img-caption { text-align: center; color: #778DA9; font-size: 14px; margin-bottom: 20px; }
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

# --- PREGUNTAS CON IMÁGENES ---
def obtener_quiz():
    return [
        {
            "p": "¿En qué año inventó Lester S. Hill este sistema?", 
            "o": ["1929", "1945", "1914", "1935"], "c": "1929",
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Lester_S._Hill.jpg/220px-Lester_S._Hill.jpg",
            "cap": "Lester S. Hill, matemático y criptógrafo estadounidense."
        },
        {
            "p": "Cifra 'MA' con la matriz del proyecto.", 
            "o": ["KY", "AT", "RI", "ZE"], "c": "KY",
            "img": "https://i.imgur.com/vH9F5tZ.png", # Tabla A=0, B=1...
            "cap": "Usa esta tabla para convertir letras a números."
        },
        {
            "p": "¿Cuál es la base del cifrado Hill?", 
            "o": ["Aritmética Modular", "Cifrado César", "Código Binario", "Física Cuántica"], "c": "Aritmética Modular",
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Modulo_clock_26.svg/300px-Modulo_clock_26.svg.png",
            "cap": "La aritmética modular funciona como un reloj de 26 horas."
        },
        {
            "p": "Si el resultado es 36, ¿cuál es su valor en Módulo 26?", 
            "o": ["10", "15", "5", "0"], "c": "10",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_6uH4FmF7u0_y89j_LpG_W5V8S_K3-Z8n-A&s",
            "cap": "Cálculo: 36 mod 26 = ?"
        },
        {
            "p": "¿Qué operación matemática usa el Cifrado Hill?", 
            "o": ["Multiplicación de Matrices", "Raíz Cuadrada", "Logaritmos", "Integrales"], "c": "Multiplicación de Matrices",
            "img": "https://i.ytimg.com/vi/v_p7Y7_G1Sg/maxresdefault.jpg",
            "cap": "Operación central: Matriz K por vector P."
        },
        {
            "p": "En el sistema Hill, la letra A es igual a...", 
            "o": ["0", "1", "26", "-1"], "c": "0",
            "img": "https://i.imgur.com/vH9F5tZ.png",
            "cap": "Recuerda que en criptografía empezamos desde cero."
        },
        {
            "p": "¿A qué número corresponde la letra 'D'?", 
            "o": ["3", "4", "2", "5"], "c": "3",
            "img": "https://i.imgur.com/vH9F5tZ.png",
            "cap": "A=0, B=1, C=2..."
        },
        {
            "p": "¿Cuál es el propósito principal del Cifrado Hill?", 
            "o": ["Criptografía", "Calcular distancias", "Arquitectura", "Música"], "c": "Criptografía",
            "img": "https://cdn.pixabay.com/photo/2017/02/10/14/06/padlock-2055198_1280.png",
            "cap": "Protección de información mediante algoritmos."
        },
        {
            "p": "Si K=10 y multiplicas por 1, ¿qué letra obtienes?", 
            "o": ["K", "A", "Z", "M"], "c": "K",
            "img": "https://i.imgur.com/vH9F5tZ.png",
            "cap": "Busca el valor 10 en la tabla."
        },
        {
            "p": "En la matriz del proyecto, ¿cuál es el valor de $K_{11}$?", 
            "o": ["5", "3", "2", "0"], "c": "5",
            "img": "https://i.imgur.com/7KqP8rO.png", # Imagen de la matriz del proyecto
            "cap": "Observa la posición fila 2, columna 2."
        }
    ]

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = obtener_quiz()

# --- PANTALLA 1: EXPLICACIÓN ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🔵 Cifrado Hill: Fundamentos Técnicos</h1>", unsafe_allow_html=True)
    st.image("https://i.ytimg.com/vi/p8p8W-p_e-k/maxresdefault.jpg", use_container_width=True)
    st.markdown("""
    ### 📂 Resumen del Proyecto
    El **Cifrado Hill** es un sistema criptográfico de sustitución basado en álgebra lineal.
    - **Representación:** $A=0, B=1, ..., Z=25$.
    - **Matriz K:** Se usa como llave de cifrado.
    - **Módulo 26:** Garantiza resultados dentro del alfabeto.
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
    
    st.markdown(f"<p style='text-align:right; color:#778DA9;'>Pregunta {st.session_state.indice + 1} / 10</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{actual['p']}</h3>", unsafe_allow_html=True)
    
    # IMAGEN DE APOYO
    st.image(actual["img"], use_container_width=True)
    st.markdown(f"<p class='img-caption'>{actual['cap']}</p>", unsafe_allow_html=True)
    
    opciones_mezcladas = st.session_state[f"opciones_{st.session_state.indice}"]
    cols = st.columns(2)
    for i, opc in enumerate(opciones_mezcladas):
        with cols[i % 2]:
            if st.button(opc):
                if opc == actual["c"]:
                    st.success("¡Bien hecho! 💎")
                    st.session_state.buenas += 1
                else:
                    st.error(f"Incorrecto. Era: {actual['c']}")
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
    st.markdown("<h1 class='main-title'>🏁 Informe de Resultados</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#1B4332; text-align:center;'><h3>Correctas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#641212; text-align:center;'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    if st.button("🔄 Reiniciar Prueba"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
