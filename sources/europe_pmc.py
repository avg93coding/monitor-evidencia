# sources/europe_pmc.py
import requests

def buscar_europe_pmc(query, max_resultados=10):
    """
    Consulta la API de Europe PMC y devuelve publicaciones o registros relacionados con el término.
    """
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "pageSize": max_resultados
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code != 200:
            return [{"ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        data = response.json()
        resultados = []

        for r in data.get("resultList", {}).get("result", []):
            resultados.append({
                "ID": r.get("id", "-"),
                "Título": r.get("title", "-"),
                "Fuente": r.get("source", "-"),
                "Tipo": r.get("pubType", "-"),
                "Enlace": f"https://europepmc.org/article/{r.get('source', 'MED')}/{r.get('id', '')}"
            })

        return resultados

    except Exception as e:
        return [{"ID": "error", "Título": f"Error en Europe PMC: {str(e)}"}]


# Prueba rápida
if __name__ == "__main__":
    res = buscar_europe_pmc("semaglutide", 5)
    for r in res:
        print(r)
