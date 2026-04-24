import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="IUE Hill Quiz - 2026", layout="centered")

# --- DISEÑO AZUL PROFESIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1B2A; color: #E0E1DD; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        font-weight: bold; background-color: #1B263B;
        color: #778DA9; border: 2px solid #415A77; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #415A77; color: #E0E1DD; border: 2px solid #778DA9; }
    .main-title { text-align: center; color: #E0E1DD; font-weight: 800; margin-bottom: 20px; }
    .question-box { background-color: #1B263B; padding: 20px; border-radius: 15px; border-left: 5px solid #415A77; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE TUS 20 PREGUNTAS ---
def obtener_todas_las_preguntas():
    return [
        {"p": "¿Qué es el cifrado Hill?", "o": ["Un método de compresión", "Un cifrado basado en matrices", "Un sistema binario", "Un método gráfico"], "c": "Un cifrado basado en matrices"},
        {"p": "¿Quién desarrolló el cifrado Hill?", "o": ["Newton", "Euclides", "Lester S. Hill", "Turing"], "c": "Lester S. Hill"},
        {"p": "¿Cómo se representan las letras en este sistema?", "o": ["A=0 hasta Z=25", "A=1 hasta Z=26", "A=2 hasta Z=27", "A=10 hasta Z=35"], "c": "A=0 hasta Z=25"},
        {"p": "¿Qué significa trabajar en módulo 26?", "o": ["Dividir entre 26", "Multiplicar por 26", "Usar números negativos", "Reducir valores entre 0 y 25"], "c": "Reducir valores entre 0 y 25"},
        {"p": "¿Qué función cumple la matriz clave?", "o": ["Ordenar letras", "Eliminar datos", "Codificar el mensaje", "Sumar valores"], "c": "Codificar el mensaje"},
        {"p": "¿Cuándo es invertible una matriz en Z₂₆?", "o": ["Siempre", "Cuando el determinante es 0", "Cuando mcd(det(K),26)=1", "Cuando es par"], "c": "Cuando mcd(det(K),26)=1"},
        {"p": "¿Qué pasa si la matriz clave no es invertible?", "o": ["No se puede descifrar", "Se mejora el cifrado", "Se vuelve más rápido", "No pasa nada"], "c": "No se puede descifrar"},
        {"p": "¿Para qué sirve la matriz inversa en este método?", "o": ["Ordenar", "Dividir", "Cifrar", "Descifrar"], "c": "Descifrar"},
        {"p": "¿Por qué se dice que es un cifrado poligráfico?", "o": ["Usa símbolos", "Trabaja con varias letras a la vez", "Usa gráficos", "Usa colores"], "c": "Trabaja con varias letras a la vez"},
        {"p": "¿Por qué no se usa actualmente en alta seguridad?", "o": ["Es muy moderno", "Es ilegal", "Es fácil de vulnerar", "Es muy lento"], "c": "Es fácil de vulnerar"},
        {"p": "¿Cuál es la representación numérica de la letra 'M'?", "o": ["11", "13", "12", "14"], "c": "12"},
        {"p": "Si la matriz K es (3 3 / 2 5), ¿cuál es su determinante?", "o": ["15", "6", "1", "9"], "c": "9"},
        {"p": "¿Cuál es el inverso de 9 en módulo 26?", "o": ["5", "3", "9", "2"], "c": "3"},
        {"p": "¿Cómo se agrupa la palabra 'MATRIZ' para cifrarla?", "o": ["MAT - RIZ", "MA - TRI - Z", "MA - TR - IZ", "M-A-T-R-I-Z"], "c": "MA - TR - IZ"},
        {"p": "¿Qué valor numérico corresponde a la letra 'Z'?", "o": ["26", "24", "0", "25"], "c": "25"},
        {"p": "¿Qué se hace si falta una letra para completar un bloque?", "o": ["Se elimina", "Se repite la última", "Se deja así", "Se rellena con X"], "c": "Se rellena con X"},
        {"p": "¿Cuál es el valor de la letra 'X' en la tabla?", "o": ["24", "22", "23", "25"], "c": "23"},
        {"p": "¿Cuál es el resultado de la operación 36 mod 26?", "o": ["12", "8", "10", "6"], "c": "10"},
        {"p": "¿Cuál es la operación principal del método?", "o": ["División", "Multiplicación de matrices", "Suma", "Resta"], "c": "Multiplicación de matrices"},
        {"p": "¿Cuál es una ventaja de usar matrices 3×3 en lugar de 2×2?", "o": ["Usa menos datos", "Es más rápido", "Es más fácil", "Es más seguro"], "c": "Es más seguro"}
    ]

# --- INICIALIZACIÓN ---
if 'jugando' not in st.session_state:
    st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.buenas = 0
    st.session_state.malas = 0
    st.session_state.terminado = False

# --- PANTALLA 1: BIENVENIDA ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🌟 ¡Bienvenidos a los juegos del Cifrado Hill!</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 📂 Instrucciones del Desafío
    Hoy pondremos a prueba lo aprendido sobre Álgebra Lineal aplicada a la criptografía.
    
    - **El Alfabeto:** Usamos el sistema $A=0, B=1, ..., Z=25$.
    - **La Matriz:** Nuestra clave es una matriz cuadrada.
    - **El Quiz:** Se elegirán 10 preguntas aleatorias de nuestra base de datos.
    """)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    if st.button("Inicio de prueba"):
        # Seleccionar 10 al azar de tus 20
        todas = obtener_todas_las_preguntas()
        st.session_state.preguntas = random.sample(todas, 10)
        st.session_state.jugando = True
        st.rerun()

# --- PANTALLA 2: EL QUIZ ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    
    if f"opciones_{st.session_state.indice}" not in st.session_state:
        ops = actual["o"].copy()
        random.shuffle(ops)
        st.session_state[f"opciones_{st.session_state.indice}"] = ops
    
    st.markdown(f"<p style='text-align:right; color:#778DA9;'>Pregunta {st.session_state.indice + 1} de 10</p>", unsafe_allow_html=True)
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
    st.markdown("<h1 class='main-title'>🏁 Informe Final</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#1B4332; text-align:center;'><h3>Buenas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#641212; text-align:center;'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    puntos = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center; margin-top:20px;'>Puntaje: {puntos} / 100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Volver a Intentar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
