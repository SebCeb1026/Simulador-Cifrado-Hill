import streamlit as st
import numpy as np
import time
import random

# Configuración de la página
st.set_page_config(page_title="IUE Hill Quiz Challenge", layout="centered")

# Estilos para que se vea más profesional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-size: 18px; font-weight: bold; }
    .main-title { text-align: center; color: #2E7D32; }
    .stat-box { padding: 20px; border-radius: 10px; text-align: center; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE PREGUNTAS (Teoría y Práctica) ---
def obtener_preguntas():
    return [
        {
            "tipo": "teoria",
            "pregunta": "¿En qué año inventó Lester S. Hill este sistema de cifrado?",
            "opciones": ["1929", "1945", "1914", "1935"],
            "correcta": "1929"
        },
        {
            "tipo": "practica",
            "pregunta": "Cifra 'MA' usando la matriz clave del proyecto.",
            "opciones": ["KY", "AT", "RI", "ZE"],
            "correcta": "KY"
        },
        {
            "tipo": "teoria",
            "pregunta": "¿Cuál es la base del cifrado Hill según el texto?",
            "opciones": ["Aritmética Modular", "Cifrado César", "Código Binario", "Física Cuántica"],
            "correcta": "Aritmética Modular"
        },
        {
            "tipo": "teoria",
            "pregunta": "En el sistema Hill, ¿cómo se representan las letras?",
            "opciones": ["Como números del 0 al 25", "Como símbolos químicos", "Como códigos de barras", "Como números del 1 al 100"],
            "correcta": "Como números del 0 al 25"
        },
        {
            "tipo": "practica",
            "pregunta": "Si el resultado de una operación es 36, ¿cuál es su valor en Módulo 26?",
            "opciones": ["10", "15", "5", "0"],
            "correcta": "10"
        },
        {
            "tipo": "teoria",
            "pregunta": "¿Qué operación matemática es el corazón del Cifrado Hill?",
            "opciones": ["Multiplicación de Matrices", "Raíz Cuadrada", "Logaritmos", "Integrales"],
            "correcta": "Multiplicación de Matrices"
        },
        {
            "tipo": "practica",
            "pregunta": "¿A qué número corresponde la letra 'D' en la tabla A=0, B=1...?",
            "opciones": ["3", "4", "2", "5"],
            "correcta": "3"
        },
        {
            "tipo": "teoria",
            "pregunta": "¿Para qué sirve el Cifrado Hill?",
            "opciones": ["Ocultar mensajes (Criptografía)", "Calcular distancias", "Diseñar edificios", "Hacer música"],
            "correcta": "Ocultar mensajes (Criptografía)"
        },
        {
            "tipo": "practica",
            "pregunta": "Si K es 10 y multiplicamos por 1, ¿qué letra obtenemos?",
            "opciones": ["K", "A", "Z", "M"],
            "correcta": "K"
        },
        {
            "tipo": "teoria",
            "pregunta": "En la matriz clave del ejercicio 1, ¿cuál es el valor de K[1,1]?",
            "opciones": ["5", "3", "2", "0"],
            "correcta": "5"
        }
    ]

# --- INICIALIZACIÓN DE VARIABLES ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.buenas = 0
    st.session_state.malas = 0
    st.session_state.preguntas = obtener_preguntas()
    st.session_state.terminado = False

# --- LÓGICA DEL QUIZ ---
st.markdown("<h1 class='main-title'>🔐 Reto Hill: Teoría y Práctica</h1>", unsafe_allow_html=True)

if not st.session_state.terminado:
    actual = st.session_state.preguntas[st.session_state.indice]
    
    st.subheader(f"Pregunta {st.session_state.indice + 1} de 10")
    st.info(actual["pregunta"])
    
    if actual["tipo"] == "practica":
        st.write("💡 *Pista: Usa la tabla A=0...Z=25 y la matriz del proyecto.*")

    # Botones de opciones
    cols = st.columns(2)
    for i, opcion in enumerate(actual["opciones"]):
        with cols[i % 2]:
            if st.button(opcion, key=f"btn_{st.session_state.indice}_{i}"):
                if opcion == actual["correcta"]:
                    st.success("¡CORRECTO! ✨")
                    st.session_state.buenas += 1
                else:
                    st.error(f"INCORRECTO ❌. La respuesta era: {actual['correcta']}")
                
                time.sleep(1.5)
                
                if st.session_state.indice < 9:
                    st.session_state.indice += 1
                else:
                    st.session_state.terminado = True
                st.rerun()

# --- RESUMEN FINAL ---
else:
    st.balloons()
    st.header("🏁 ¡Desafío Completado!")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='stat-box'><h3>✅ Correctas</h3><h1 style='color:green'>{st.session_state.buenas}</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><h3>❌ Incorrectas</h3><h1 style='color:red'>{st.session_state.malas}</h1></div>", unsafe_allow_html=True)
    
    total = st.session_state.buenas * 10
    st.subheader(f"Puntaje Final: {total} / 100")
    
    if st.button("Intentar de nuevo"):
        st.session_state.indice = 0
        st.session_state.buenas = 0
        st.session_state.malas = 0
        st.session_state.terminado = False
        st.rerun()
