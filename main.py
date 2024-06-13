# TODO
# Set up Google Web Searcher class
# Set up proper Chroma DB collection
# Set up LLM lookup agent

from earnest import Earnest
from knowledge_base import KnowledgeBase, RequestType


# Load Documents
url = "https://s27.q4cdn.com/749715820/files/doc_financials/2023/q4/a31f2915-31bf-45ae-99cf-18f3c0138869.pdf"
ex1 = (RequestType.SCRAPE, url)

search_request = "Tesla Q4 2023 earnings report 10-k"
ex2 = (RequestType.SEARCH, search_request)

knowledge_base = KnowledgeBase(ex1)
earnest_llm = Earnest(knowledge_base)

question = "What was SoFi's Total Net Revenue this quarter?"
print(earnest_llm.ask(question))
