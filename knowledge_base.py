import re
from typing import Optional

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.tools import tool

from utils import setup_openai
from web_search import fetch_knowledge, load_and_split_urls
from enum import Enum


setup_openai()


class RequestType(Enum):
    SCRAPE = 0
    SEARCH = 1


class KnowledgeBase:
    def __init__(self):
        self.vectorstore = Chroma(embedding_function=OpenAIEmbeddings())

    def enrich_knowledge_base(self, search_query: str):
        # Query the DB for answers
        if search_query[0] == RequestType.SCRAPE:
            url = search_query[1]
            # Load, split, embed & store
            docs = self.scrape_info(url)
        elif search_query[0] == RequestType.SEARCH:
            query = search_query[1]
            docs = fetch_knowledge(query)
        
        self._add_to_knowledge_base(docs)

    @tool
    def scrape_info(self, query: str) -> list[Document]:
        """
        Used when user provides a URL to retrieve information

        :param query: query from user
        """
        urls = KnowledgeBase.find_urls(query)

        documents = []
        for url in urls:
            file_extension = KnowledgeBase._identify_file_extension(url)
            if file_extension == "pdf":
                documents += KnowledgeBase._load_and_transform_pdf(url)
            else:
                documents += load_and_split_urls(url)

        return documents

    @tool
    def web_search(self, query: str):
        """
        Used to search the web and
        add retrieved documents to knowledge base

        :param query: query from user
        """
        documents = fetch_knowledge(query)
        
        return documents

    @staticmethod
    def _load_and_transform_pdf(urls: list[str]) -> list[Document]:
        # Load & transform PDF
        loader = PyPDFLoader(urls)
        documents = loader.load_and_split()

        return documents

    @staticmethod
    def _identify_file_extension(url: str):
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

    def _add_to_knowledge_base(self, docs: Document):
        # Enrich the knowledge base with retrieved documents
        self.vectorstore.add_documents(documents=docs)
