# sources/clinical_trials_scraper.py
import requests
from bs4 import BeautifulSoup


def buscar_trials_scraping(query, max_resultados=10):
    """
    Realiza scraping desde ClinicalTrials.gov y extrae una lista de estudios básicos.
    """
    base_url = "https://clinicaltrials.gov/search"
    params = {
        "intr": query.strip(),
        "count": max_resultados  # no limita realmente, pero es buena práctica
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        soup = BeautifulSoup(response.text, "html.parser")
        resultados = []

        cards = soup.find_all("a", class_="ct-result-card")
        for card in cards[:max_resultados]:
            try:
                titulo = card.find("h3").get_text(strip=True)
                estado_tag = card.find("span", class_="ct-result-status")
                estado = estado_tag.get_text(strip=True) if estado_tag else "-"
                enlace = "https://clinicaltrials.gov" + card.get("href", "")
                nct_id = enlace.split("/")[-1] if enlace else "-"

                resultados.append({
                    "NCT ID": nct_id,
                    "Título": titulo,
                    "Estado": estado,
                    "Enlace": enlace
                })
            except Exception:
                continue  # ignorar errores de parsing individuales

        if not resultados:
            return [{"NCT ID": "sin_datos", "Título": "No se encontraron resultados visibles."}]

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error en scraping: {str(e)}"}]


# Prueba rápida local
if __name__ == "__main__":
    res = buscar_trials_scraping("semaglutide", 5)
    for r in res:
        print(r)
