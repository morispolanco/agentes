import streamlit as st

st.set_page_config(page_title="Plataforma de Agentes de IA", page_icon="🤖")

st.title("Plataforma de Agentes de IA")
st.write("""
Bienvenido a la plataforma para crear y chatear con agentes de inteligencia artificial que siguen tus instrucciones.
  
- **Crear Agente**: Define las instrucciones y asigna un nombre único al agente.
- **Chat con Agente**: Interactúa en tiempo real con el agente configurado.
""")

# Mostrar la lista de agentes existentes (opcional)
if 'agents' in st.session_state and len(st.session_state['agents']) > 0:
    st.subheader("Agentes Configurados")
    for idx, agent in enumerate(st.session_state['agents'], 1):
        st.markdown(f"{idx}. **{agent['name']}**")
else:
    st.info("Aún no hay agentes configurados. Ve a la página **Crear Agente de IA** para comenzar.")
