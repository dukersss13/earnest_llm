import re

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from utils import setup_openai
from web_search import fetch_knowledge, transform_search_results
from enum import Enum


setup_openai()

class RequestType(Enum):
    SEARCH = 0
    LOAD = 1


class KnowledgeBase:
    def db_query(self, search_query: str):
        # Query the DB for answers
        if search_query[0] == RequestType.LOAD:
            url = search_query[1]
            # Load, split, embed & store
            docs = self._load_and_split(url)
        elif search_query[0] == RequestType.SEARCH:
            query = search_query[1]
            docs = fetch_knowledge(query)

        self.enrich_knowledge_base(docs)

    @staticmethod
    def _load_and_split(url: str) -> list[Document]:
        file_extension = KnowledgeBase._identify_file_extension(url)

        if file_extension == "pdf":
            loader = PyPDFLoader(url)
            documents = loader.load_and_split()
        elif file_extension == "html":
            documents = transform_search_results(url)

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

    def enrich_knowledge_base(self, docs: Document):
        """_summary_

        :param documents: _description_
        """
        self.vectorstore = Chroma.from_documents(documents=docs, 
                                                 embedding=OpenAIEmbeddings())