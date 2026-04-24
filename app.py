import streamlit as st
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Simulador Cifrado Hill", layout="centered")

st.title("🔐 Simulador Cifrado Hill - IUE")
st.markdown("Basado en el proyecto de Álgebra Lineal 2026[cite: 1, 12].")

# --- FUNCIONES DE APOYO ---
def text_to_nums(text):
    return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]

def nums_to_text(nums):
    return "".join([chr(int(n) % 26 + ord('A')) for n in nums])

def get_mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# --- MENÚ LATERAL ---
st.sidebar.header("Configuración")
dimension = st.sidebar.selectbox("Dimensión de la Matriz", [2, 3])
modo = st.sidebar.radio("Operación", ["Cifrar", "Descifrar"])

# --- ENTRADA DE DATOS ---
st.subheader("1. Configura tu Matriz Clave (K)")
cols = st.columns(dimension)
matrix_values = []
for i in range(dimension):
    with cols[i]:
        for j in range(dimension):
            val = st.number_input(f"K[{i},{j}]", value=0, key=f"k{i}{j}")
            matrix_values.append(val)

key_matrix = np.array(matrix_values).reshape(dimension, dimension)

mensaje_input = st.text_input("2. Escribe tu mensaje:", value="MATRIZ" if dimension == 2 else "ALGEBRA")

# --- PROCESAMIENTO ---
if st.button("Ejecutar Aplicación"):
    # Validar determinante [cite: 40, 44]
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    inv_det = get_mod_inverse(det, 26)
    
    if inv_det is None:
        st.error(f"⚠️ Matriz inválida: El determinante modular es {det}, el cual no tiene inverso en mod 26. El descifrado sería imposible[cite: 40].")
    else:
        nums = text_to_nums(mensaje_input)
        # Relleno (Padding) con X [cite: 34, 76]
        while len(nums) % dimension != 0:
            nums.append(23)
        
        matrix_to_use = key_matrix
        if modo == "Descifrar":
            # Cálculo de la inversa modular 
            adjugate = np.round(np.linalg.det(key_matrix) * np.linalg.inv(key_matrix)).astype(int)
            matrix_to_use = (inv_det * adjugate) % 26
            st.info("Utilizando Matriz Inversa para descifrar.")

        # Aplicar transformación lineal C = K * P (mod 26) [cite: 37]
        res_nums = []
        for i in range(0, len(nums), dimension):
            block = np.array(nums[i:i+dimension])
            res_block = np.dot(matrix_to_use, block) % 26
            res_nums.extend(res_block)
        
        resultado = nums_to_text(res_nums)
        st.success(f"### Resultado {modo}ado: {resultado}")
        st.json({"Matriz utilizada": matrix_to_use.tolist(), "Determinante modular": det})
