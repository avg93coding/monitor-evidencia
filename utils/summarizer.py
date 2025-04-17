from transformers import pipeline

# Cargar el modelo solo una vez
resumidor = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def resumir_texto(texto):
    if not texto or texto.strip() == "":
        return "Resumen no disponible."

    prompt = "summarize: " + texto.strip()
    
    try:
        resumen = resumidor(prompt, max_length=100, min_length=30, do_sample=False)
        return resumen[0]['summary_text']
    except Exception as e:
        return f"⚠️ Error al resumir texto: {str(e)}"
