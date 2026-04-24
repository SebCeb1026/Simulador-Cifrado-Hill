import streamlit as st
import numpy as np
import time
import random

# Configuración de página con icono de candado
st.set_page_config(page_title="IUE - Hill Cipher Challenge", page_icon="🔐", layout="centered")

# --- DISEÑO UI AVANZADO (AZUL TECNOLÓGICO) ---
st.markdown("""
    <style>
    /* Fondo con degradado sutil */
    .stApp { 
        background: linear-gradient(135deg, #0D1B2A 0%, #1B263B 100%);
        color: #E0E1DD;
    }
    
    /* Tarjeta de pregunta */
    .question-card {
        background-color: #1B263B;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #415A77;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        text-align: center;
    }

    /* Estilo de los botones de opciones */
    .stButton>button { 
        width: 100%; 
        border-radius: 15px; 
        height: 4em; 
        font-weight: 600; 
        font-size: 16px;
        background-color: #0D1B2A;
        color: #778DA9;
        border: 2px solid #415A77;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    
    .stButton>button:hover {
        background-color: #415A77;
        color: white;
        border: 2px solid #E0E1DD;
        transform: translateY(-2px);
    }

    /* Títulos y textos */
    .main-title { 
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center; 
        color: #E0E1DD; 
        font-weight: 800; 
        letter-spacing: 1px;
    }
    
    /* Barra de progreso personalizada */
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
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
        {"p": "¿Cuál es una ventaja de usar matrices 3×3?", "o": ["Usa menos datos", "Es más rápido", "Es más fácil", "Es más seguro"], "c": "Es más seguro"}
    ]

# --- LÓGICA DE ESTADO ---
if 'jugando' not in st.session_state: st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.buenas = 0
    st.session_state.malas = 0
    st.session_state.terminado = False

# --- PANTALLA DE INICIO ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🔵 IUE: Hill Cipher Game</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pon a prueba tus conocimientos en Álgebra Lineal</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style='background-color:#1B263B; padding:20px; border-radius:15px; border-left:5px solid #1E88E5;'>
        <strong>Resumen Técnico:</strong><br>
        1. A=0, B=1... Z=25.<br>
        2. La clave es la matriz K.<br>
        3. Usamos Módulo 26 para todas las operaciones.
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    if st.button("Inicio de prueba"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()

# --- PANTALLA DE JUEGO ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    
    # Barra de progreso
    progreso = (st.session_state.indice) / 10
    st.progress(progreso)
    st.markdown(f"<p style='text-align:center; font-size:12px; color:#778DA9;'>Progreso: {st.session_state.indice}/10</p>", unsafe_allow_html=True)

    # Tarjeta de Pregunta
    st.markdown(f"""
    <div class='question-card'>
        <h2 style='color:#E0E1DD; margin-bottom:0;'>{actual['p']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if f"opciones_{st.session_state.indice}" not in st.session_state:
        ops = actual["o"].copy()
        random.shuffle(ops)
        st.session_state[f"opciones_{st.session_state.indice}"] = ops
    
    opciones = st.session_state[f"opciones_{st.session_state.indice}"]
    cols = st.columns(2)
    for i, opc in enumerate(opciones):
        with cols[i % 2]:
            if st.button(opc):
                if opc == actual["c"]:
                    st.toast("¡Correcto! 💎", icon="✅")
                    st.session_state.buenas += 1
                else:
                    st.toast("Incorrecto ❌", icon="⚠️")
                    st.session_state.malas += 1
                
                time.sleep(0.5)
                if st.session_state.indice < 9: st.session_state.indice += 1
                else: st.session_state.terminado = True
                st.rerun()

# --- PANTALLA FINAL ---
else:
    st.balloons()
    st.markdown("<h1 class='main-title'>🏁 ¡Resultados Finales!</h1>", unsafe_allow_html=True)
    
    res_cols = st.columns(2)
    with res_cols[0]:
        st.markdown(f"<div style='background-color:#1B4332; padding:20px; border-radius:20px; text-align:center;'><h3>✅ Aciertos</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with res_cols[1]:
        st.markdown(f"<div style='background-color:#641212; padding:20px; border-radius:20px; text-align:center;'><h3>❌ Fallos</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center; margin-top:30px;'>Puntaje Total: {total}/100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Reiniciar Desafío"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
