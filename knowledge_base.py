import re

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


class KnowledgeBase:
    def __init__(self, url: str):
        # Load, split, embed & store
        pages = self._load_and_split(url)
        self.vectorstore = Chroma.from_documents(documents=pages, 
                                                 embedding=OpenAIEmbeddings())

    @staticmethod
    def _load_and_split(url: str):
        file_extension = KnowledgeBase._identify_file_extension(url)

        if file_extension == "pdf":
            loader = PyPDFLoader(url)
        elif file_extension == "html":
            pass

        pages = loader.load_and_split()

        return pages

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
