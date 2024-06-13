from utils import setup_google_search, setup_openai

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents import Document


setup_google_search()
setup_openai()

search = GoogleSearchAPIWrapper()


def conduct_websearch(query: str) -> list[str]:
    """_summary_

    :param query: _description_
    :return: _description_
    """
    r = search.results(query, num_results=6)
    urls = [link["link"] for link in r]

    return urls


def transform_search_results(urls: list[str]):
    # Load HTML
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs)
    
    return docs_transformed


def fetch_knowledge(query: str) -> list[Document]:
    """_summary_

    :param query: _description_
    :return: _description_
    """
    urls = conduct_websearch(query)
    docs = transform_search_results(urls)

    return docs
