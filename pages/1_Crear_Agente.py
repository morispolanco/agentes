import streamlit as st

st.set_page_config(page_title="Crear Agente de IA", page_icon="✍️")

st.title("Crear Agente de IA")

st.write("""
Define las instrucciones que el agente de inteligencia artificial seguirá durante las interacciones.
""")

# Área de texto para las instrucciones del sistema
system_instructions = st.text_area(
    "Instrucciones para el Agente de IA",
    "You are a helpful assistant."
)

# Botón para guardar las instrucciones
if st.button("Guardar Instrucciones"):
    if system_instructions.strip() == "":
        st.error("Por favor, ingresa unas instrucciones válidas.")
    else:
        # Guardar las instrucciones en el estado de la sesión
        st.session_state['system_instructions'] = system_instructions
        st.success("Instrucciones guardadas exitosamente.")
