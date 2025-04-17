# sources/clinical_trials_scraper.py
import requests
from bs4 import BeautifulSoup

def buscar_trials_scraping(query, max_resultados=10):
    base_url = "https://clinicaltrials.gov/search"
    params = {
        "intr": query.strip(),
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}", "Enlace": "https://clinicaltrials.gov"}]

        soup = BeautifulSoup(response.text, "html.parser")
        resultados = []

        tarjetas = soup.find_all("a", class_="hit-card-title")
        for tarjeta in tarjetas[:max_resultados]:
            titulo = tarjeta.get_text(strip=True)
            href = tarjeta.get("href", "")
            enlace = f"https://clinicaltrials.gov{href}" if href else "#"
            nct_id = href.split("/study/")[-1].split("?")[0] if "/study/" in href else "-"

            resultados.append({
                "NCT ID": nct_id,
                "Título": titulo,
                "Estado": "-",  # No disponible directamente en este nivel
                "Enlace": enlace
            })

        if not resultados:
            return [{"NCT ID": "sin_datos", "Título": "No se encontraron resultados visibles.", "Enlace": "https://clinicaltrials.gov"}]

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error en scraping: {str(e)}", "Enlace": "https://clinicaltrials.gov"}]

# Prueba rápida
if __name__ == "__main__":
    res = buscar_trials_scraping("semaglutide", 5)
    for r in res:
        print(r)
