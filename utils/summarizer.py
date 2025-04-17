import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    def resumir_texto(texto):
        return "🔒 Gemini API Key no configurada."
else:
    genai.configure(api_key=api_key)

    def resumir_texto(texto):
        if not texto.strip():
            return "Resumen no disponible."

        try:
            model = genai.GenerativeModel("models/chat-bison-001")
            chat = model.start_chat()
            prompt = f"Resume en 3 a 5 líneas, con lenguaje técnico claro, el siguiente abstract académico:\n\n{texto.strip()}"
            response = chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error al generar resumen con Gemini (chat-bison): {str(e)}"
