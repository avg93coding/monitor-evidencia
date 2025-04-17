# clinical_trials.py
import requests
import pandas as pd

def buscar_trials(query, max_resultados=10):
    """
    Consulta la API de ClinicalTrials.gov y devuelve una lista con estudios clínicos relacionados.
    """
    url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": query,
        "fields": "NCTId,BriefTitle,Condition,OverallStatus,Phase,LocationCountry,StartDate",
        "min_rnk": 1,
        "max_rnk": max_resultados,
        "fmt": "json"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        try:
            data = response.json()
        except ValueError:
            return [{"NCT ID": "error", "Título": "Respuesta inválida de ClinicalTrials.gov"}]

        resultados = []
        for study in data["StudyFieldsResponse"].get("StudyFields", []):
            nct_id = study.get("NCTId", [""])[0]
            resultados.append({
                "NCT ID": nct_id,
                "Título": study.get("BriefTitle", [""])[0],
                "Condición": ", ".join(study.get("Condition", [])),
                "Estado": study.get("OverallStatus", [""])[0],
                "Fase": study.get("Phase", [""])[0],
                "País": ", ".join(study.get("LocationCountry", [])),
                "Fecha de inicio": study.get("StartDate", [""])[0],
                "Enlace": f"https://clinicaltrials.gov/ct2/show/{nct_id}"
            })

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error al buscar en ClinicalTrials.gov: {str(e)}"}]


# Prueba rápida (se puede eliminar para producción)
if __name__ == "__main__":
    resultados = buscar_trials("semaglutide", max_resultados=5)
    for r in resultados:
        print(r)# clinical_trials.py
import requests
import pandas as pd

def buscar_trials(query, max_resultados=10):
    """
    Consulta la API de ClinicalTrials.gov y devuelve una lista con estudios clínicos relacionados.
    """
    url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": query,
        "fields": "NCTId,BriefTitle,Condition,OverallStatus,Phase,LocationCountry,StartDate",
        "min_rnk": 1,
        "max_rnk": max_resultados,
        "fmt": "json"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        try:
            data = response.json()
        except ValueError:
            return [{"NCT ID": "error", "Título": "Respuesta inválida de ClinicalTrials.gov"}]

        resultados = []
        for study in data["StudyFieldsResponse"].get("StudyFields", []):
            nct_id = study.get("NCTId", [""])[0]
            resultados.append({
                "NCT ID": nct_id,
                "Título": study.get("BriefTitle", [""])[0],
                "Condición": ", ".join(study.get("Condition", [])),
                "Estado": study.get("OverallStatus", [""])[0],
                "Fase": study.get("Phase", [""])[0],
                "País": ", ".join(study.get("LocationCountry", [])),
                "Fecha de inicio": study.get("StartDate", [""])[0],
                "Enlace": f"https://clinicaltrials.gov/ct2/show/{nct_id}"
            })

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error al buscar en ClinicalTrials.gov: {str(e)}"}]


# Prueba rápida (se puede eliminar para producción)
if __name__ == "__main__":
    resultados = buscar_trials("semaglutide", max_resultados=5)
    for r in resultados:
        print(r)# clinical_trials.py
import requests
import pandas as pd

def buscar_trials(query, max_resultados=10):
    """
    Consulta la API de ClinicalTrials.gov y devuelve una lista con estudios clínicos relacionados.
    """
    url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": query,
        "fields": "NCTId,BriefTitle,Condition,OverallStatus,Phase,LocationCountry,StartDate",
        "min_rnk": 1,
        "max_rnk": max_resultados,
        "fmt": "json"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return [{"NCT ID": "error", "Título": f"Error HTTP {response.status_code}"}]

        try:
            data = response.json()
        except ValueError:
            return [{"NCT ID": "error", "Título": "Respuesta inválida de ClinicalTrials.gov"}]

        resultados = []
        for study in data["StudyFieldsResponse"].get("StudyFields", []):
            nct_id = study.get("NCTId", [""])[0]
            resultados.append({
                "NCT ID": nct_id,
                "Título": study.get("BriefTitle", [""])[0],
                "Condición": ", ".join(study.get("Condition", [])),
                "Estado": study.get("OverallStatus", [""])[0],
                "Fase": study.get("Phase", [""])[0],
                "País": ", ".join(study.get("LocationCountry", [])),
                "Fecha de inicio": study.get("StartDate", [""])[0],
                "Enlace": f"https://clinicaltrials.gov/ct2/show/{nct_id}"
            })

        return resultados

    except Exception as e:
        return [{"NCT ID": "error", "Título": f"Error al buscar en ClinicalTrials.gov: {str(e)}"}]


# Prueba rápida (se puede eliminar para producción)
if __name__ == "__main__":
    resultados = buscar_trials("semaglutide", max_resultados=5)
    for r in resultados:
        print(r)
