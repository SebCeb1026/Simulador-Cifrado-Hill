import streamlit as st
import numpy as np
import time
import random

st.set_page_config(page_title="Hill Quiz - IUE", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .big-font { font-size:20px !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIO / EXPLICACIÓN ---
st.title("🔐 Cifrado Hill: El Desafío IUE")
st.write("Basado en el proyecto de Álgebra Lineal 2026[cite: 1, 12].")

with st.expander("📖 REPASO RÁPIDO (Lee antes de jugar)"):
    st.write("Para cifrar usamos la fórmula: $C = K \cdot P \pmod{26}$[cite: 37].")
    st.write("1. **Convertir:** A=0, B=1, C=2, ... Z=25[cite: 32].")
    st.write("2. **Multiplicar:** Matriz $\\times$ Vector.")
    st.write("3. **Módulo:** El resto de dividir por 26.")
    st.info("Ejemplo: con $K = \\begin{pmatrix} 3 & 3 \\\\ 2 & 5 \\end{pmatrix}$, la palabra **MA** (12, 0) se convierte en **KY** (10, 24)[cite: 53].")

# --- LÓGICA DEL JUEGO ---
if 'preg_n' not in st.session_state:
    st.session_state.preg_n = 1
    st.session_state.puntos = 0
    st.session_state.finalizado = False

def generar_pregunta():
    palabras = ["MA", "TR", "IZ", "BE", "LA", "HE", "ID", "AD", "GO", "SI"]
    palabra = palabras[st.session_state.preg_n - 1]
    K = np.array([[3, 3], [2, 5]])
    
    # Calcular respuesta correcta
    nums = [ord(c) - ord('A') for c in palabra]
    res_nums = np.dot(K, np.array(nums)) % 26
    correcta = "".join([chr(int(n) + ord('A')) for n in res_nums])
    
    # Generar opciones falsas
    opciones = [correcta]
    while len(opciones) < 4:
        falsa = "".join([chr(random.randint(0, 25) + ord('A')) for _ in range(2)])
        if falsa not in opciones:
            opciones.append(falsa)
    random.shuffle(opciones)
    return palabra, correcta, opciones

# --- PANTALLA DE JUEGO ---
if st.session_state.preg_n <= 10 and not st.session_state.finalizado:
    palabra, correcta, opciones = generar_pregunta()
    
    st.subheader(f"Pregunta {st.session_state.preg_n} de 10")
    st.markdown(f"<p class='big-font'>Cifra la palabra: '{palabra}'</p>", unsafe_allow_html=True)
    st.write("Usando $K = \\begin{pmatrix} 3 & 3 \\\\ 2 & 5 \\end{pmatrix}$")
    
    # Mostrar opciones en botones
    cols = st.columns(2)
    for i, opc in enumerate(opciones):
        with cols[i % 2]:
            if st.button(f"{chr(65+i)}) {opc}"):
                if opc == correcta:
                    st.session_state.puntos += 10
                    st.success("¡Correcto!")
                else:
                    st.error(f"Incorrecto. Era {correcta}")
                
                time.sleep(1)
                st.session_state.preg_n += 1
                st.rerun()

# --- PANTALLA FINAL ---
else:
    st.balloons()
    st.header("🎊 ¡Juego Terminado!")
    st.metric("Puntaje Final", f"{st.session_state.puntos} / 100")
    
    if st.button("Reiniciar Desafío"):
        st.session_state.preg_n = 1
        st.session_state.puntos = 0
        st.session_state.finalizado = False
        st.rerun()
