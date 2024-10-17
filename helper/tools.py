import re
from langchain_core.documents import Document
from langchain_community.document_loaders.pdf import PyPDFLoader
from helper.web_search import load_and_split_urls


def scrape_info(urls: list[str]) -> list[Document]:
    """
    Used when user provides a URL to retrieve information

    :param query: query from user
    """
    documents = []
    for url in urls:
        file_extension = identify_file_extension(url)
        if file_extension == "pdf":
            documents += load_and_transform_pdf(url)
        else:
            documents += load_and_split_urls(url)

    return documents

def load_and_transform_pdf(urls: list[str]) -> list[Document]:
    # Load & transform PDF
    loader = PyPDFLoader(urls)
    documents = loader.load_and_split()

    return documents

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