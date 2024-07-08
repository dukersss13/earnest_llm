import re
from langchain_core.documents import Document
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.tools import tool
from web_search import fetch_knowledge, load_and_split_urls


@tool
def scrape_info(query: str) -> list[Document]:
    """
    Used when user provides a URL to retrieve information

    :param query: query from user
    """
    urls = find_urls(query)

    documents = []
    for url in urls:
        file_extension = identify_file_extension(url)
        if file_extension == "pdf":
            documents += load_and_transform_pdf(url)
        else:
            documents += load_and_split_urls(url)

    return documents

@tool
def web_search(query: str):
    """
    Used to search the web
    when the user specifically asks for 
    a "search" or "look up"

    :param query: query from user
    """
    documents = fetch_knowledge(query)
    
    return documents

@tool
def answer(rag_chain, query: str):
    """
    Used when the user asks a question

    :param query: query from user
    """
    return rag_chain.invoke(query)


def load_and_transform_pdf(urls: list[str]) -> list[Document]:
    # Load & transform PDF
    loader = PyPDFLoader(urls)
    documents = loader.load_and_split()

    return documents

@staticmethod
def identify_file_extension(url: str):
    # Regex pattern to match common document file extensions
    pattern = re.compile(r'\.(pdf|html?|docx?|xlsx?|pptx?|txt|rtf|odt|csv|json|xml|md)$', re.IGNORECASE)
    
    # Search for the pattern in the URL
    match = pattern.search(url)
    
    if match:
        # Return the file extension (without the dot)
        return match.group(1)
    else:
        # Return None if no valid extension is found
        return None


@staticmethod
def find_urls(text) -> list[str]:
    # Define the URL regex pattern
    url_pattern = re.compile(
        r'http[s]?://'                     # http:// or https://
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|' # domain...
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'    # ...or percent-encoded characters
    )
    # Find all matches in the text
    urls = re.findall(url_pattern, text)
    
    return urls