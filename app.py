import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz - Full Color", layout="centered")

# --- DISEÑO DE COLORES PERSONALIZADO ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #f4f7f6; }
    
    /* Botones de opciones */
    .stButton>button { 
        width: 100%; 
        border-radius: 15px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: #ffffff;
        color: #1E88E5;
        border: 2px solid #1E88E5;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E88E5;
        color: white;
    }
    
    /* Títulos y textos */
    .main-title { text-align: center; color: #0D47A1; font-family: 'Arial'; }
    .question-text { font-size: 22px; font-weight: bold; color: #333; text-align: center; }
    
    /* Cajas de resumen */
    .good-box { padding: 20px; border-radius: 10px; background-color: #C8E6C9; border: 2px solid #4CAF50; text-align: center; }
    .bad-box { padding: 20px; border-radius: 10px; background-color: #FFCDD2; border: 2px solid #F44336; text-align: center; }
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
    st.markdown("<h1 class='main-title'>🔐 Introducción al Cifrado Hill</h1>", unsafe_allow_html=True)
    st.info("""
    ### 📝 Guía Rápida para Ganar:
    1. **Letras ↔ Números:** A=0, B=1... hasta Z=25.
    2. **Fórmula:** $C = K \cdot P \pmod{26}$.
    3. **Matrices:** Se multiplica la matriz clave por la palabra.
    4. **El Reloj:** Si el resultado pasa de 26, se busca el residuo (Módulo 26).
    """)
    st.warning("⚠️ **Dato clave:** La respuesta correcta cambia de lugar en cada turno.")
    
    if st.button("🎮 ¡EMPEZAR DESAFÍO!"):
        st.session_state.jugando = True
        st.rerun()

# --- PANTALLA 2: EL QUIZ ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    
    # Aleatorizar opciones solo una vez por pregunta
    if f"opciones_{st.session_state.indice}" not in st.session_state:
        ops = actual["o"].copy()
        random.shuffle(ops)
        st.session_state[f"opciones_{st.session_state.indice}"] = ops
    
    st.markdown(f"<p style='text-align:right; color:grey;'>Pregunta {st.session_state.indice + 1} de 10</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='question-text'>{actual['p']}</p>", unsafe_allow_html=True)
    
    opciones_mezcladas = st.session_state[f"opciones_{st.session_state.indice}"]
    
    cols = st.columns(2)
    for i, opc in enumerate(opciones_mezcladas):
        with cols[i % 2]:
            if st.button(opc):
                if opc == actual["c"]:
                    st.toast("¡Excelente! 🎯", icon="✅")
                    st.session_state.buenas += 1
                else:
                    st.toast(f"Error ❌. Era: {actual['c']}", icon="⚠️")
                    st.session_state.malas += 1
                
                time.sleep(1)
                if st.session_state.indice < 9:
                    st.session_state.indice += 1
                else:
                    st.session_state.terminado = True
                st.rerun()

# --- PANTALLA 3: RESUMEN FINAL ---
else:
    st.balloons()
    st.markdown("<h1 class='main-title'>🏁 ¡Resultados Finales!</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='good-box'><h3>Correctas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='bad-box'><h3>Incorrectas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center;'>Tu Puntaje: {total}/100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Reiniciar Aplicación"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
