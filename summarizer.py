# utils/summarizer.py
import os
from openai import OpenAI
from utils.secure_config import get_openai_api_key

def resumir_texto(texto, max_tokens=150):
    """
    Función para resumir texto usando OpenAI API con manejo seguro de API key.
    """
    # Get API key securely
    api_key = get_openai_api_key()
    
    if not api_key:
        return "⚠️ API key no configurada. Por favor ingresa tu API key en la sección de Configuración."
    
    try:
        # Inicializar el cliente de OpenAI con la clave API
        client = OpenAI(api_key=api_key)
        
        # Llamar a la API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente científico que resume artículos médicos de forma concisa y precisa."},
                {"role": "user", "content": f"Resume el siguiente texto científico en español en aproximadamente 3-4 oraciones clave:\n\n{texto}"}
            ],
            max_tokens=max_tokens
        )
        
        # Extraer el contenido de la respuesta
        return response.choices[0].message.content
            
    except Exception as e:
        return f"Error al resumir texto: {str(e)}"