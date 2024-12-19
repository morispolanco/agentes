import streamlit as st

st.set_page_config(page_title="Crear Agente de IA", page_icon="✍️")

st.title("Crear Agente de IA")

st.write("""
Define las instrucciones que el agente de inteligencia artificial seguirá durante las interacciones y asígnale un nombre único.
""")

# Área de texto para el nombre del agente
agent_name = st.text_input("Nombre del Agente de IA:", "")

# Área de texto para las instrucciones del sistema
system_instructions = st.text_area(
    "Instrucciones para el Agente de IA",
    "You are a helpful assistant."
)

# Botón para guardar las instrucciones
if st.button("Guardar Agente"):
    if agent_name.strip() == "":
        st.error("Por favor, ingresa un nombre válido para el agente.")
    elif system_instructions.strip() == "":
        st.error("Por favor, ingresa unas instrucciones válidas.")
    else:
        # Inicializar la lista de agentes si no existe
        if 'agents' not in st.session_state:
            st.session_state['agents'] = []

        # Verificar si el nombre ya existe
        existing_names = [agent['name'] for agent in st.session_state['agents']]
        if agent_name in existing_names:
            st.error("Ya existe un agente con este nombre. Por favor, elige un nombre diferente.")
        else:
            # Agregar el nuevo agente a la lista
            st.session_state['agents'].append({
                "name": agent_name,
                "instructions": system_instructions,
                "conversation": []
            })
            st.success(f"Agente '{agent_name}' guardado exitosamente.")
