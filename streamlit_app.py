import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Longevity Intelligence Monitor",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Longevity Intelligence Monitor")

KEYWORDS = [
    "longevity",
    "aging",
    "senolytics",
    "rapamycin",
    "healthspan",
    "epigenetic reprogramming"
]

keyword = st.selectbox(
    "Tema",
    KEYWORDS
)


@st.cache_data(ttl=3600)
def search_pubmed(term):

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={term}"
        "&retmode=json&retmax=20"
    )

    response = requests.get(url)
    data = response.json()

    return data["esearchresult"]["idlist"]


@st.cache_data(ttl=3600)
def get_paper_details(ids):

    if not ids:
        return pd.DataFrame()

    id_string = ",".join(ids)

    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esummary.fcgi?db=pubmed&id={id_string}"
        "&retmode=json"
    )

    response = requests.get(url)
    data = response.json()

    papers = []

    for paper_id in ids:

        item = data["result"].get(paper_id, {})

        papers.append(
            {
                "Título": item.get("title", ""),
                "Revista": item.get("fulljournalname", ""),
                "Fecha": item.get("pubdate", ""),
                "PubMed": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/"
            }
        )

    return pd.DataFrame(papers)


ids = search_pubmed(keyword)

st.metric(
    "Papers encontrados",
    len(ids)
)

if ids:

    papers_df = get_paper_details(ids)

    st.subheader("Artículos encontrados")

    st.dataframe(
        papers_df,
        use_container_width=True
    )

else:
    st.warning("No se encontraron resultados")