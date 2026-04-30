import streamlit as st
import numpy as np
import time
import random

# Configuración de página con icono de seguridad
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
    /* Fondo con gradiente profundo */
    .stApp { 
        background: radial-gradient(circle, #1b263b 0%, #0d1b2a 100%);
        color: #E0E1DD;
    }
    
    /* Tarjeta tipo Cristal */
    .glass-card {
        background: rgba(27, 38, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
        text-align: center;
    }

    /* Botones Interactivos */
    .stButton>button { 
        width: 100%; 
        border-radius: 18px; 
        height: 4.5em; 
        font-weight: 700; 
        font-size: 16px;
        background: rgba(65, 90, 119, 0.2);
        color: #E0E1DD;
        border: 1px solid #778DA9;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .stButton>button:hover {
        background: #415A77;
        color: #ffffff;
        border: 1px solid #E0E1DD;
        transform: scale(1.03);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* Estilo de texto y títulos */
    .main-title { 
        font-size: 45px;
        text-align: center; 
        background: -webkit-linear-gradient(#E0E1DD, #778DA9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    .result-win { border: 2px solid #4ADE80; background: rgba(74, 222, 128, 0.15); padding: 30px; border-radius: 25px; text-align:center; }
    .result-lose { border: 2px solid #F87171; background: rgba(248, 113, 113, 0.15); padding: 30px; border-radius: 25px; text-align:center; }
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

# --- LÓGICA DE ESTADO ---
if 'jugando' not in st.session_state: st.session_state.jugando = False
if 'indice' not in st.session_state:
    st.session_state.indice, st.session_state.buenas, st.session_state.malas = 0, 0, 0
    st.session_state.terminado = False

# --- 1. PANTALLA INICIAL (ACTUALIZADA) ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🛡️ CIFRADO HILL: PROTOCOLO TÉCNICO</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color:#4ADE80; margin-bottom:15px; text-align:center;'>Explicación del Sistema</h3>
        <p style='text-align:justify; color:#E0E1DD; line-height:1.6;'>
            ¡Bienvenidos al desafío de Criptografía! Este juego consiste en un <b>Banco de Preguntas</b> técnicas sobre el cifrado Hill. 
            Deberás responder un total de <b>10 preguntas</b> seleccionadas al azar. Para ganar la prueba, es necesario acertar al menos <b>6 de ellas</b>; de lo contrario, habrás reprobado el sistema de seguridad.
        </p>
        
        <div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border-left: 5px solid #778DA9; text-align:left;'>
            <h4 style='color:#778DA9; margin-top:0;'>📊 Conceptos Clave</h4>
            <ul style='color:#BDC3C7; font-size:14px;'>
                <li><b>Alfabeto:</b> Las letras se mapean de <b>A=0</b> hasta <b>Z=25</b>.</li>
                <li><b>Aritmética Modular:</b> Todas las operaciones se realizan bajo el módulo 26.</li>
                <li><b>Matrices:</b> La seguridad depende de la multiplicación de vectores por una matriz clave.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r"K_{clave} = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    if st.button("🚀 INICIAR EVALUACIÓN"):
        st.session_state.preguntas = random.sample(obtener_todas_las_preguntas(), 10)
        st.session_state.jugando = True
        st.rerun()

# --- 2. PANTALLA JUEGO ---
elif not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    st.progress(st.session_state.indice / 10)
    
    st.markdown(f"""
    <div class='glass-card'>
        <p style='color:#778DA9;'>Reto N° {st.session_state.indice + 1} de 10</p>
        <h2 style='margin-top:0;'>{actual['p']}</h2>
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
            if st.button(opc, key=f"btn_{st.session_state.indice}_{i}"):
                if opc == actual["c"]:
                    reproducir_efecto("https://www.myinstants.com/media/sounds/level-up-mario.mp3")
                    st.toast("¡Correcto!", icon="✨")
                    st.session_state.buenas += 1
                else:
                    reproducir_efecto("https://www.myinstants.com/media/sounds/mario-bros-die.mp3")
                    st.toast("Fallaste", icon="💀")
                    st.session_state.malas += 1
                
                time.sleep(1.0)
                if st.session_state.indice < 9: 
                    st.session_state.indice += 1
                else: 
                    st.session_state.terminado = True
                st.rerun()

# --- 3. PANTALLA RESULTADOS ---
else:
    # Cálculo de nota sobre 100
    puntaje = st.session_state.buenas * 10
    
    if st.session_state.buenas >= 6:
        st.balloons()
        reproducir_efecto("https://www.myinstants.com/media/sounds/victory-mario-series.mp3")
        st.markdown(f"""
            <div class='result-win'>
                <h1 style='font-size: 50px;'>🎖️ PRUEBA SUPERADA</h1>
                <p>Has demostrado dominio técnico sobre el Cifrado Hill.</p>
                <hr style='border: 0.5px solid #4ADE80; opacity: 0.3;'>
                <h2>NOTA FINAL: {puntaje} / 100</h2>
                <p style='color:#4ADE80;'>Aciertos: {st.session_state.buenas} de 10</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        reproducir_efecto("https://www.myinstants.com/media/sounds/game-over-mario-bros.mp3")
        st.markdown(f"""
            <div class='result-lose'>
                <div style='font-size: 80px;'>😞</div>
                <h1>PRUEBA REPROBADA</h1>
                <p>No has alcanzado el mínimo de 6 aciertos necesarios.</p>
                <hr style='border: 0.5px solid #F87171; opacity: 0.3;'>
                <h2>NOTA FINAL: {puntaje} / 100</h2>
                <p style='color:#F87171;'>Aciertos: {st.session_state.buenas} de 10</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 REINICIAR EVALUACIÓN"):
        # Limpiar todo el estado para volver a empezar
        for key in list(st.session_state.keys()): 
            del st.session_state[key]
        st.rerun()
