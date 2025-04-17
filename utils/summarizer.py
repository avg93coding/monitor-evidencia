from transformers import pipeline

# Cargar el pipeline una sola vez al iniciar la app
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def resumir_texto(texto):
    if not texto.strip():
        return "Resumen no disponible."

    try:
        entrada = "summarize: " + texto.strip()
        resultado = summarizer(entrada, max_length=100, min_length=30, do_sample=False)
        return resultado[0]['summary_text']
    except Exception as e:
        return f"⚠️ Error al generar resumen: {str(e)}"
