from Bio import Entrez
from Bio import Medline

Entrez.email = "tucorreo@ejemplo.com"  # Cambia por tu correo real

def buscar_pubmed(query, max_resultados=10):
    """Busca artículos en PubMed por palabra clave y devuelve resumen estructurado."""
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_resultados)
        record = Entrez.read(handle)
        id_list = record.get("IdList", [])

        resultados = []

        if not id_list:
            return resultados

        fetch_handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="medline", retmode="text")
        records = Medline.parse(fetch_handle)

        for r in records:
            resultados.append({
                "PMID": r.get("PMID", ""),
                "Título": r.get("TI", "Sin título disponible"),
                "Autores": ", ".join(r.get("AU", [])),
                "Resumen": r.get("AB", "Resumen no disponible."),
                "Fuente": r.get("SO", "")
            })

        return resultados

    except Exception as e:
        return [{"PMID": "error", "Título": "Error al buscar en PubMed", "Resumen": str(e), "Autores": "", "Fuente": ""}]
