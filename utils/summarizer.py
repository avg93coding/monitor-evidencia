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
            model = genai.GenerativeModel(model_name="models/chat-bison-001")
            response = model.generate_message(
                contents=[
                    {
                        "role": "user",
                        "parts": [f"Resume en 3 a 5 líneas el siguiente abstract académico:\n\n{texto.strip()}"]
                    }
                ]
            )
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error al generar resumen con Gemini (chat-bison): {str(e)}"
