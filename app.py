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
    .matrix-style { font-size: 24px; text-align: center; color: #415A77; font-weight: bold; }
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

# --- PREGUNTAS (Sin códigos técnicos) ---
def obtener_quiz():
    return [
        {"p": "¿En qué año se creó oficialmente este sistema de cifrado?", "o": ["1929", "1945", "1914", "1935"], "c": "1929"},
        {"p": "Si usas la matriz del proyecto, ¿cuál es el resultado de cifrar 'MA'?", "o": ["KY", "AT", "RI", "ZE"], "c": "KY"},
        {"p": "¿Cómo se llama el método que usa el residuo de la división por 26?", "o": ["Aritmética Modular", "Cálculo Integral", "Álgebra de Boole", "Trigonometría"], "c": "Aritmética Modular"},
        {"p": "Si el cálculo da 36, ¿qué número queda tras aplicar el Módulo 26?", "o": ["10", "15", "5", "0"], "c": "10"},
        {"p": "¿Qué herramienta matemática es la 'llave' en este cifrado?", "o": ["Las Matrices", "Las Derivadas", "Los Vectores", "Las Integrales"], "c": "Las Matrices"},
        {"p": "En nuestra tabla de conversión, ¿qué número le asignamos a la letra 'A'?", "o": ["0", "1", "26", "A"], "c": "0"},
        {"p": "Si contamos A=0, B=1, C=2... ¿Qué número le toca a la letra 'D'?", "o": ["3", "4", "2", "5"], "c": "3"},
        {"p": "¿Cuál es el objetivo principal de este sistema?", "o": ["Protección de mensajes", "Diseño de puentes", "Contabilidad", "Creación de música"], "c": "Protección de mensajes"},
        {"p": "Si una operación da 10, ¿qué letra buscamos en la tabla?", "o": ["K", "A", "Z", "M"], "c": "K"},
        {"p": "En nuestra matriz, ¿qué número está en la esquina inferior derecha?", "o": ["5", "3", "2", "0"], "c": "5"}
    ]

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = obtener_quiz()

# --- PANTALLA 1: BIENVENIDA Y EXPLICACIÓN ---
if not st.session_state.jugando:
    st.markdown("<h1 class='main-title'>🌟 ¡Bienvenidos a los juegos del Cifrado Hill!</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 📂 ¿Cómo funciona nuestro proyecto?
    Antes de empezar, repasemos la base técnica que utilizamos para proteger la información:
    
    1. **El Alfabeto Numérico:** Cada letra se convierte en un número empezando desde cero ($A=0, B=1, ..., Z=25$).
    2. **La Matriz Clave:** Usamos esta matriz para transformar los datos:
    """)
    
    # Matriz visualmente bonita
    st.latex(r"K = \begin{pmatrix} 3 & 3 \\ 2 & 5 \end{pmatrix}")
    
    st.markdown("""
    3. **Aritmética Modular:** Aplicamos el **Módulo 26** a los resultados. Esto es como un reloj: si el número es mayor a 25, volvemos a empezar desde el cero para encontrar la letra correcta.
    
    *¿Estás listo para poner a prueba tus conocimientos?*
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
    st.markdown("<h1 class='main-title'>🏁 ¡Fin del Desafío!</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#1B4332; text-align:center;'><h3>Buenas</h3><h1>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#641212; text-align:center;'><h3>Malas</h3><h1>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.markdown(f"<h2 style='text-align:center; margin-top:20px;'>Puntaje: {total} / 100</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 Volver a Intentar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
