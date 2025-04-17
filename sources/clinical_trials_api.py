# sources/clinical_trials_api.py
import requests

def buscar_trials_api(query, max_resultados=10):
    """
    Consulta la API JSON interna de ClinicalTrials.gov (no oficial, pero pública y funcional).
    """
    base_url = "https://clinicaltrials.gov/api/v1/studies"
    params = {
        "term": query.strip(),
        "page": 1,
        "size": max_resultados
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        data = response.json()
        estudios = data.get("studies", [])
        resultados = []

        for estudio in estudios[:max_resultados]:
            resultados.append({
                "NCT ID": estudio.get("nctId", "-"),
                "Título": estudio.get("studyTitle", "-"),
                "Estado": estudio.get("recruitmentStatus", "-"),
                "Fase": estudio.get("phase", "-"),
                "Patrocinador": estudio.get("sponsor", {}).get("name", "-"),
                "Enlace": f"https://clinicaltrials.gov/study/{estudio.get('nctId', '-')}",
            })

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error en API interna: {str(e)}"}]


# Prueba local
if __name__ == "__main__":
    res = buscar_trials_api("semaglutide", 5)
    for r in res:
        print(r)
