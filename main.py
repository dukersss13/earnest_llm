# TODO
# Set up Google Web Searcher class
# Set up proper Chroma DB collection
# Set up LLM lookup agent

from earnest import Earnest
from knowledge_base import KnowledgeBase

# Load Documents
url = "https://s27.q4cdn.com/749715820/files/doc_financials/2023/q4/a31f2915-31bf-45ae-99cf-18f3c0138869.pdf"

knowledge_base = KnowledgeBase(url)
earnest_llm = Earnest(knowledge_base)

question = "What was SoFi's revenue this quarter?"
print(earnest_llm.ask(question))
