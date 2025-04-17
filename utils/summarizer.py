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
            model = genai.GenerativeModel(model_name="models/text-bison-001")  # <- compatible y estable
            prompt = f"Resume el siguiente texto científico en 3 a 5 líneas:\n\n{texto.strip()}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error al generar resumen con Gemini: {str(e)}"
