import streamlit as st
import requests
import json

st.set_page_config(page_title="Chat con el Agente de IA", page_icon="💬")

st.title("Chat con el Agente de IA")

st.write("""
Interactúa con tu agente de inteligencia artificial configurado.
""")

# Verificar si las instrucciones del agente están configuradas
if 'system_instructions' not in st.session_state:
    st.warning("Por favor, ve a la página **Crear Agente de IA** para configurar tu agente antes de iniciar el chat.")
else:
    # Área de texto para el input del usuario
    user_input = st.text_input("Tú:", "")

    # Contenedor para mostrar la conversación
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []

    if user_input:
        # Agregar el mensaje del usuario a la conversación
        st.session_state['conversation'].append({"role": "user", "content": user_input})

        # Mostrar el mensaje del usuario
        st.write(f"**Tú:** {user_input}")

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
                        "content": st.session_state['system_instructions']
                    }
                ] + st.session_state['conversation'],
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
                    st.session_state['conversation'].append({"role": "assistant", "content": ai_response})
                    # Mostrar la respuesta del agente
                    st.write(f"**Agente de IA:** {ai_response}")
                else:
                    st.error(f"Error en la solicitud: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
