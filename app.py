import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz - Blue Edition", layout="centered")

# --- DISEÑO TOTAL BLUE ---
st.markdown("""
    <style>
    /* Fondo general en azul muy oscuro */
    .stApp { 
        background-color: #0D1B2A; 
        color: #E0E1DD;
    }
    
    /* Estilo de los botones */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.8em; 
        font-weight: bold; 
        background-color: #1B263B;
        color: #778DA9;
        border: 2px solid #415A77;
        transition: 0.4s;
    }
    
    /* Efecto al pasar el mouse por los botones */
    .stButton>button:hover {
        background-color: #415A77;
        color: #E0E1DD;
        border: 2px solid #778DA9;
    }
    
    /* Títulos */
    .main-title { text-align: center; color: #E0E1DD; font-family: 'Segoe UI'; font-weight: 800; }
    
    /* Cajas de texto y alertas */
    .stAlert { background-color: #1B263B; color: #E0E1DD; border: 1px solid #415A77; }
    
    /* Resumen final */
    .good-box { padding: 20px; border-radius: 15px; background-color: #1B4332; border: 2px solid #2D6A4F; text-align: center; }
    .bad-box { padding: 20px; border-radius: 15px; background-color: #641212; border: 2px solid #A4161A; text-align: center; }
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

# --- PREGUNTAS ---
def obtener_quiz():
    return [
        {"p": "¿En qué año inventó Lester S. Hill este sistema?", "o": ["1929", "1945", "1914", "1935"], "c": "1929"},
        {"p": "Cifra 'MA' con la matriz del proyecto ($K_{00}=3, K_{01}=3...$)", "o": ["KY", "AT", "RI", "ZE"], "c": "KY"},
        {"p": "¿Cuál es la base del cifrado Hill?", "o": ["Aritmética Modular", "Cifrado César", "Código Binario", "Física Cuántica"], "c": "Aritmética Modular"},
        {"p": "Si el resultado es 36, ¿cuál es su valor en Módulo 26?", "o": ["10", "15", "5", "0"], "c": "10"},
        {"p": "¿Qué operación matemática usa el Cifrado Hill?", "o": ["Multiplicación de Matrices", "Raíz Cuadrada", "Logaritmos", "Integrales"], "c": "Multiplicación de Matrices"},
        {"p": "En el sistema Hill, la letra A es igual a...", "o": ["0", "1", "26", "-1"], "c": "0"},
        {"p": "¿A qué número corresponde la letra 'D'?", "o": ["3", "4", "2", "5"], "c": "3"},
        {"p": "¿Cuál es el propósito principal del Cifrado Hill?", "o": ["Criptografía", "Calcular distancias", "Arquitectura", "Música"], "c": "Criptografía"},
        {"p": "Si K=10 y multiplicas por 1, ¿qué letra obtienes?", "o": ["K", "A", "Z", "M"], "c": "K"},
        {"p": "En la matriz del proyecto, ¿cuál es el valor de $K_{11}$?", "o": ["5", "3", "2", "0"], "c": "5"}
    ]

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = obtener_quiz()

# --- PANTALLA 1: EXPLICACIÓN ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🔵 IUE: Cifrado Hill Challenge</h1>", unsafe_allow_html=True)
    st.write("Bienvenido al reto de Álgebra Lineal. Repasa antes de empezar:")
    st.info("""
    - **Alfabeto:** A=0, B=1, ..., Z=25.
    - **Lógica:** Multiplicamos matrices y aplicamos Módulo 26.
    - **Clave:** La matriz del proyecto es de $2 \\times 2$.
    """)
    st.warning("Las respuestas cambiarán de posición en cada pregunta. ¡Mucha suerte!")
    
    if st.button("🔵 INICIAR DESAFÍO AZUL"):
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
    with c1:
        st.markdown(f"<div class='good-box'><h3>Correctas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='bad-box'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center; margin-top:20px;'>Puntaje Total: {total}/100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Reiniciar Prueba"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
