# app.py

import streamlit as st
import requests
import json

# Título de la aplicación
st.title("Generador de Agentes de IA")

# Descripción
st.write("""
Esta plataforma permite generar agentes de inteligencia artificial que siguen las instrucciones proporcionadas.
""")

# Entrada de usuario para las instrucciones
user_instructions = st.text_area("Ingresa las instrucciones para el agente de IA:", 
                                 "Testing. Just say hi and hello world and nothing else.")

# Botón para generar la respuesta
if st.button("Generar Respuesta"):
    if user_instructions.strip() == "":
        st.error("Por favor, ingresa unas instrucciones válidas.")
    else:
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
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": user_instructions
                    }
                ],
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
                    st.success("Respuesta del Agente de IA:")
                    st.write(ai_response)
                else:
                    st.error(f"Error en la solicitud: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
