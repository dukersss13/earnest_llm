from helper.config import SEARCH_ENGINE, Search
from helper.utils import setup_google_search, setup_openai, setup_tavily_search

from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


setup_openai()


if SEARCH_ENGINE == Search.GOOGLE:
    setup_google_search()
    search = GoogleSearchAPIWrapper()
elif SEARCH_ENGINE == Search.TAVILY:
    setup_tavily_search()
    search = TavilySearchResults(max_results=4)


def conduct_websearch(query: str) -> list[str]:
    """
    Conduct a web search using GoogleSearchAPI
    """
    if SEARCH_ENGINE == Search.GOOGLE:
        r = search.results(query, num_results=4)
        urls = [link["link"] for link in r]
    elif SEARCH_ENGINE == Search.TAVILY:
        r = search.invoke(query)
        urls = [link["url"] for link in r]

    return urls


def load_and_split_urls(urls: list[str]):
    """
    Load and transform found documents
    """
    loader = WebBaseLoader(urls)
    docs = loader.load()
    docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    
    return docs


def fetch_knowledge(query: str) -> list[Document]:
    """
    Conduct a web search and store information
    in vector database
    """
    urls = conduct_websearch(query)
    docs = load_and_split_urls(urls)

    return docs
