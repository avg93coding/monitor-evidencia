import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    def resumir_texto(texto):
        return "🔒 Gemini API Key no configurada."
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    def resumir_texto(texto):
        if not texto.strip():
            return "Resumen no disponible."
        try:
            prompt = f"Resume en 3 a 5 líneas el siguiente abstract científico:\n\n{texto.strip()}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error al generar resumen con Gemini: {str(e)}"
