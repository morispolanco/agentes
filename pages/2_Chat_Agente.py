import streamlit as st
import requests
import json

st.set_page_config(page_title="Chat con el Agente de IA", page_icon="💬")

st.title("Chat con el Agente de IA")

st.write("""
Interactúa con tus agentes de inteligencia artificial configurados.
""")

# Verificar si existen agentes configurados
if 'agents' not in st.session_state or len(st.session_state['agents']) == 0:
    st.warning("No hay agentes configurados. Ve a la página **Crear Agente de IA** para crear uno.")
else:
    # Seleccionar el agente con el que se desea chatear
    agent_names = [agent['name'] for agent in st.session_state['agents']]
    selected_agent_name = st.selectbox("Selecciona el Agente con el que deseas chatear:", agent_names)

    # Obtener el agente seleccionado
    selected_agent = next((agent for agent in st.session_state['agents'] if agent['name'] == selected_agent_name), None)

    if selected_agent:
        # Área de texto para el input del usuario
        user_input = st.text_input("Tú:", "")

        if 'conversation' not in selected_agent:
            selected_agent['conversation'] = []

        if user_input:
            # Agregar el mensaje del usuario a la conversación
            selected_agent['conversation'].append({"role": "user", "content": user_input})

            # Mostrar el mensaje del usuario
            st.markdown(f"**Tú:** {user_input}")

            # Mostrar un spinner mientras se procesa la solicitud
            with st.spinner("Generando respuesta..."):
                # URL de la API
                api_url = "https://api.x.ai/v1/chat/completions"

                # Cabeceras de la solicitud
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {st.secrets['xai_api_key']}"
                }

                # Cuerpo de la solicitud
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": selected_agent['instructions']
                        }
                    ] + selected_agent['conversation'],
                    "model": "grok-2-1212",
                    "stream": False,
                    "temperature": 0.7
                }

                try:
                    # Realizar la solicitud POST
                    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

                    # Verificar el estado de la respuesta
                    if response.status_code == 200:
                        response_data = response.json()
                        # Asumiendo que la respuesta tiene una clave 'choices' con 'message' y 'content'
                        ai_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No se recibió respuesta.')
                        # Agregar la respuesta del agente a la conversación
                        selected_agent['conversation'].append({"role": "assistant", "content": ai_response})
                        # Mostrar la respuesta del agente
                        st.markdown(f"**{selected_agent_name}:** {ai_response}")
                    else:
                        st.error(f"Error en la solicitud: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")

        # Mostrar la conversación completa
        st.markdown("### Conversación")
        for message in selected_agent['conversation']:
            role = "Tú" if message['role'] == 'user' else selected_agent_name
            st.markdown(f"**{role}:** {message['content']}")
