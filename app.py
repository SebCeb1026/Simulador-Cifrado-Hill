import streamlit as st
import numpy as np
import time
import random

# Configuración de página
st.set_page_config(page_title="IUE - Hill Cipher Challenge", page_icon="🔐", layout="centered")

# --- DISEÑO UI ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0D1B2A 0%, #1B263B 100%); color: #E0E1DD; }
    .question-card {
        background-color: #1B263B; padding: 30px; border-radius: 20px;
        border: 1px solid #415A77; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px; text-align: center;
    }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 3.8em; font-weight: 600; 
        background-color: #0D1B2A; color: #778DA9; border: 2px solid #415A77; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #415A77; color: white; border: 2px solid #E0E1DD; }
    .win-box { background-color: #1B4332; padding: 30px; border-radius: 20px; border: 2px solid #4ADE80; text-align: center; }
    .lose-box { background-color: #4A0E0E; padding: 30px; border-radius: 20px; border: 2px solid #F87171; text-align: center; }
    .sad-face { font-size: 100px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE PREGUNTAS ---
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

# --- LÓGICA ---
if 'jugando' not in st.session_state: st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice, st.session_state.buenas, st.session_state.malas = 0, 0, 0
    st.session_state.terminado = False

# --- PANTALLA INICIAL ---
if not st.session_state.jugando:
    st.markdown("<h1 style='text-align:center;'>🔐 IUE: Hill Cipher Game</h1>", unsafe_allow_html=True)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    if st.button("Inicio de prueba"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()

# --- PANTALLA JUEGO ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    st.progress(st.session_state.indice / 10)
    st.markdown(f"<div class='question-card'><h2>{actual['p']}</h2></div>", unsafe_allow_html=True)
    
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
                    st.toast("¡Bien!", icon="✅")
                    st.session_state.buenas += 1
                else:
                    st.toast("Mal", icon="❌")
                    st.session_state.malas += 1
                time.sleep(0.3)
                if st.session_state.indice < 9: st.session_state.indice += 1
                else: st.session_state.terminado = True
                st.rerun()

# --- PANTALLA RESULTADOS ---
else:
    puntaje = st.session_state.buenas * 10
    
    if puntaje >= 60:
        st.balloons()
        st.markdown(f"""
            <div class='win-box'>
                <h1 style='color: #4ADE80;'>¡Felicidades! 🏆</h1>
                <p>Has aprobado la prueba de criptografía.</p>
                <h2 style='margin:0;'>Nota: {puntaje} / 100</h2>
            </div>
        """, unsafe_allow_html=True)
        # Audio de Victoria (Opcional: puedes cambiar el link por uno de tu preferencia)
        st.audio("https://www.myinstants.com/media/sounds/victory-mario-series.mp3")
    else:
        st.markdown(f"""
            <div class='lose-box'>
                <div class='sad-face'>😞</div>
                <h1 style='color: #F87171;'>No has aprobado</h1>
                <p>Tu puntaje fue insuficiente. ¡Debes repasar!</p>
                <h2 style='margin:0;'>Nota: {puntaje} / 100</h2>
            </div>
        """, unsafe_allow_html=True)
        # Audio de Error
        st.audio("https://www.myinstants.com/media/sounds/mario-dies.mp3")
    
    if st.button("🔄 Volver a Intentar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
