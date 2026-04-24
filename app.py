import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="Hill Challenge IUE", layout="centered")

# --- TÍTULO Y EXPLICACIÓN CORTA ---
st.title("🔐 Cifrado Hill: El Desafío")

with st.expander("📖 Haz clic aquí para aprender cómo jugar (Explicación rápida)"):
    st.markdown("""
    El **Cifrado Hill** usa álgebra lineal para proteger mensajes. 
    1. **Convertir:** Cada letra es un número (A=0, B=1, C=2...).
    2. **Multiplicar:** Multiplicamos una **matriz clave** por los números de la palabra.
    3. **Módulo 26:** Al resultado se le aplica el residuo de dividir por 26 para que siempre sea una letra.
    
    **Ejemplo rápido:** Si la matriz es $\\begin{pmatrix} 3 & 3 \\\\ 2 & 5 \\end{pmatrix}$ y la palabra es **MA** (12, 0):
    * $3(12) + 3(0) = 36 \\rightarrow$ en módulo 26 es **10 (K)**.
    * $2(12) + 5(0) = 24 \\rightarrow$ en módulo 26 es **24 (Y)**.
    * **Resultado:** KY.
    """)

st.divider()

# --- LÓGICA DEL JUEGO ---
if 'puntos' not in st.session_state:
    st.session_state.puntos = 0
if 'reto_actual' not in st.session_state:
    st.session_state.palabra = random.choice(["MA", "TR", "IZ", "BE", "LA"])
    st.session_state.K = np.array([[3, 3], [2, 5]])
    st.session_state.inicio = time.time()

# --- INTERFAZ DEL JUEGO ---
col1, col2 = st.columns([1, 1])
with col1:
    st.metric("🏆 Puntaje", st.session_state.puntos)
with col2:
    tiempo_transcurrido = time.time() - st.session_state.inicio
    tiempo_restante = max(0, 60 - int(tiempo_transcurrido))
    st.metric("⏳ Tiempo", f"{tiempo_restante}s")

st.info(f"### RETO: Cifra la palabra '{st.session_state.palabra}'")
st.write("Usa la matriz del proyecto: $K = \\begin{pmatrix} 3 & 3 \\\\ 2 & 5 \\end{pmatrix}$")

# Entrada de respuesta
respuesta = st.text_input("Tu respuesta (2 letras):", key="ans").upper()

if st.button("Comprobar"):
    # Validación matemática
    nums = [ord(c) - ord('A') for c in st.session_state.palabra]
    res_nums = np.dot(st.session_state.K, np.array(nums)) % 26
    correcta = "".join([chr(int(n) + ord('A')) for n in res_nums])

    if respuesta == correcta:
        st.success(f"¡Excelente! {st.session_state.palabra} es {correcta}. +10 puntos")
        st.session_state.puntos += 10
        st.balloons()
        time.sleep(2)
        # Generar nuevo reto
        st.session_state.palabra = random.choice(["HE", "ID", "AD", "GO"])
        st.session_state.inicio = time.time()
        st.rerun()
    else:
        st.error("¡Casi! Revisa la multiplicación y el módulo 26.")

if tiempo_restante == 0:
    st.warning("¡Se acabó el tiempo! Dale a 'Reiniciar' para volver a intentar.")
    if st.button("Reiniciar Juego"):
        st.session_state.puntos = 0
        st.session_state.inicio = time.time()
        st.rerun()
