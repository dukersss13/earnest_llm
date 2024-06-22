# TODO
# Set up Google Web Searcher class
# Set up proper Chroma DB collection
# Set up LLM lookup agent

from earnest import Earnest


# Load Documents
url = "https://s27.q4cdn.com/749715820/files/doc_financials/2023/q4/a31f2915-31bf-45ae-99cf-18f3c0138869.pdf"

search_request = "Tesla Q4 2023 earnings report 10-k PDF"

earnest_llm = Earnest()

question = "What was Tesla's Net Income in 2023?"
query = f"Here is the link to the earnings report {url}"

earnest_llm.ask(query)
