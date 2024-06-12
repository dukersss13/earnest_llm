from langchain_google_community import GoogleSearchAPIWrapper
from utils import setup_google_search, setup_openai


setup_google_search()
setup_openai()

search = GoogleSearchAPIWrapper()

search_request = "Tesla Q4 2023 earnings report 10-k"
r = search.results(search_request, num_results=6)

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

urls = [link["link"] for link in r]

# Load HTML
loader = AsyncHtmlLoader(urls)
docs = loader.load()

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(docs)
docs_transformed[0].page_content[0:500]


from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

db = Chroma.from_documents(documents=docs_transformed, embedding=OpenAIEmbeddings())

# Connect this to knowledge base
