import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    def resumir_texto(texto):
        return "🔒 Gemini API Key no configurada."
else:
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        def resumir_texto(texto):
            return f"❌ Error cargando modelo Gemini: {str(e)}"
    else:
        def resumir_texto(texto):
            if not texto.strip():
                return "Resumen no disponible."
            try:
                prompt = f"Resume en 3 a 5 líneas, en lenguaje técnico claro, el siguiente abstract académico:\n\n{texto.strip()}"
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                return f"⚠️ Error al generar resumen con Gemini: {str(e)}"
