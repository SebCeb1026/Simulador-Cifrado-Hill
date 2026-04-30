import streamlit as st
import numpy as np
import time
import random

# Configuración de página
st.set_page_config(page_title="IUE Hill Cipher", page_icon="🛡️", layout="centered")

# --- FUNCIÓN PARA SONIDO ---
def reproducir_efecto(url):
    st.components.v1.html(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mp3">
        </audio>
    """, height=0)

# --- DISEÑO UI AVANZADO ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1b263b 0%, #0d1b2a 100%);
        color: #E0E1DD;
    }
    
    .glass-card {
        background: rgba(27, 38, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
    }

    /* Estilo para los nuevos módulos de info */
    .info-module {
        background: rgba(65, 90, 119, 0.15);
        border: 1px solid #778DA9;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: 0.3s;
    }
    .info-module:hover {
        border-color: #4ADE80;
        background: rgba(74, 222, 128, 0.05);
    }

    .stButton>button { 
        width: 100%; border-radius: 18px; height: 4.5em; font-weight: 700; 
        font-size: 16px; background: rgba(65, 90, 119, 0.2); color: #E0E1DD;
        border: 1px solid #778DA9; transition: 0.4s;
    }
    
    .stButton>button:hover {
        background: #415A77; color: #ffffff; transform: scale(1.02);
    }

    .main-title { 
        font-size: 40px; text-align: center; font-weight: 900;
        background: linear-gradient(90deg, #E0E1DD, #778DA9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .result-win { border: 2px solid #4ADE80; background: rgba(74, 222, 128, 0.1); padding: 30px; border-radius: 25px; text-align:center; }
    .result-lose { border: 2px solid #F87171; background: rgba(248, 113, 113, 0.1); padding: 30px; border-radius: 25px; text-align:center; }
    </style>
    """, unsafe_allow_html=True)

# --- PREGUNTAS ---
def obtener_todas_las_preguntas():
    return [
        {"p": "¿Qué es el cifrado Hill?", "o": ["Un método de compresión", "Un cifrado basado en matrices", "Un sistema binario", "Un método gráfico"], "c": "Un cifrado basado en matrices"},
        {"p": "¿Cómo se representan las letras en este sistema?", "o": ["A=0 hasta Z=25", "A=1 hasta Z=26", "A=2 hasta Z=27", "A=10 hasta Z=35"], "c": "A=0 hasta Z=25"},
        {"p": "¿Qué significa trabajar en módulo 26?", "o": ["Dividir entre 26", "Multiplicar por 26", "Usar números negativos", "Reducir valores entre 0 y 25"], "c": "Reducir valores entre 0 y 25"},
        {"p": "¿Cuándo es invertible una matriz en Z₂₆?", "o": ["Siempre", "Cuando el determinante es 0", "Cuando mcd(det(K),26)=1", "Cuando es par"], "c": "Cuando mcd(det(K),26)=1"},
        {"p": "¿Por qué se dice que es un cifrado poligráfico?", "o": ["Usa símbolos", "Trabaja con varias letras a la vez", "Usa gráficos", "Usa colores"], "c": "Trabaja con varias letras a la vez"},
        {"p": "¿Cuál es la representación numérica de la letra 'M'?", "o": ["11", "13", "12", "14"], "c": "12"},
        {"p": "Si la matriz K es (3 3 / 2 5), ¿cuál es su determinante?", "o": ["15", "6", "1", "9"], "c": "9"},
        {"p": "¿Cómo se agrupa la palabra 'MATRIZ' para cifrarla?", "o": ["MAT - RIZ", "MA - TRI - Z", "MA - TR - IZ", "M-A-T-R-I-Z"], "c": "MA - TR - IZ"},
        {"p": "¿Qué se hace si falta una letra para completar un bloque?", "o": ["Se elimina", "Se repite la última", "Se deja así", "Se rellena con X"], "c": "Se rellena con X"},
        {"p": "¿Cuál es la operación principal del método?", "o": ["División", "Multiplicación de matrices", "Suma", "Resta"], "c": "Multiplicación de matrices"}
    ]

# Lógica de estado
if 'jugando' not in st.session_state: st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice, st.session_state.buenas, st.session_state.malas = 0, 0, 0
    st.session_state.terminado = False

# --- 1. PANTALLA INICIAL ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ CIFRADO HILL: CHALLENGE</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color:#4ADE80; text-align:center;'>REGLAS DE EVALUACIÓN</h3>
        <p style='text-align:center; color:#BDC3C7;'>
            Has ingresado al banco de pruebas criptográficas. Para validar tus conocimientos en el <b>Protocolo Hill</b>, deberás superar el siguiente análisis:
        </p>
        <div style='display: flex; justify-content: space-around; gap: 10px; margin-top: 20px;'>
            <div style='text-align:center;'>
                <h2 style='margin:0; color:#4ADE80;'>10</h2>
                <small style='color:#778DA9;'>PREGUNTAS</small>
            </div>
            <div style='text-align:center;'>
                <h2 style='margin:0; color:#4ADE80;'>60%</h2>
                <small style='color:#778DA9;'>PARA APROBAR</small>
            </div>
            <div style='text-align:center;'>
                <h2 style='margin:0; color:#4ADE80;'>Z₂₆</h2>
                <small style='color:#778DA9;'>MODALIDAD</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # NUEVA SECCIÓN DE "CONCEPTOS CLAVE" (SIN LISTAS ABURRIDAS)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='info-module'>
            <span style='font-size:25px;'>🔠</span><br>
            <b style='color:#E0E1DD;'>ALFABETO</b><br>
            <small style='color:#BDC3C7;'>Mapeo estándar de<br><b>A=0</b> a <b>Z=25</b></small>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""<div class='info-module'>
            <span style='font-size:25px;'>🔢</span><br>
            <b style='color:#E0E1DD;'>MÓDULO</b><br>
            <small style='color:#BDC3C7;'>Operaciones bajo<br><b>Residuo 26</b></small>
        </div>""", unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<div class='info-module'>
            <span style='font-size:25px;'>📐</span><br>
            <b style='color:#E0E1DD;'>MATRIZ</b><br>
            <small style='color:#BDC3C7;'>Transformación por<br><b>Prod. Matricial</b></small>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")

    if st.button("🚀 INICIAR EVALUACIÓN"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()

# --- 2. PANTALLA JUEGO ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    st.progress(st.session_state.indice / 10)
    
    st.markdown(f"<div class='glass-card'><p style='color:#778DA9;'>PROCESANDO RETO {st.session_state.indice + 1}</p><h2>{actual['p']}</h2></div>", unsafe_allow_html=True)
    
    if f"opciones_{st.session_state.indice}" not in st.session_state:
        ops = actual["o"].copy()
        random.shuffle(ops)
        st.session_state[f"opciones_{st.session_state.indice}"] = ops
    
    opciones = st.session_state[f"opciones_{st.session_state.indice}"]
    cols = st.columns(2)
    for i, opc in enumerate(opciones):
        with cols[i % 2]:
            if st.button(opc, key=f"btn_{i}"):
                if opc == actual["c"]:
                    reproducir_efecto("https://www.myinstants.com/media/sounds/level-up-mario.mp3")
                    st.toast("CORRECTO", icon="✅")
                    st.session_state.buenas += 1
                else:
                    reproducir_efecto("https://www.myinstants.com/media/sounds/mario-bros-die.mp3")
                    st.toast("INCORRECTO", icon="❌")
                
                time.sleep(0.8)
                if st.session_state.indice < 9: st.session_state.indice += 1
                else: st.session_state.terminado = True
                st.rerun()

# --- 3. RESULTADOS ---
else:
    puntaje = st.session_state.buenas * 10
    if st.session_state.buenas >= 6:
        st.balloons()
        st.markdown(f"<div class='result-win'><h1>🎖️ SISTEMA ACCEDIDO</h1><h2>NOTA: {puntaje}/100</h2><p>Acceso concedido al protocolo Hill.</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-lose'><h1>🚨 ACCESO DENEGADO</h1><h2>NOTA: {puntaje}/100</h2><p>Conocimientos insuficientes para el cifrado.</p></div>", unsafe_allow_html=True)
    
    if st.button("🔄 REINTENTAR"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
