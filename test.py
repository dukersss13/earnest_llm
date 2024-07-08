from utils import setup_openai
from earnest import llm
from tools import scrape_info, web_search


setup_openai()

tools = [scrape_info, web_search]

model_with_tools = llm.bind_tools(tools)

url = "https://s27.q4cdn.com/749715820/files/doc_financials/2023/q4/a31f2915-31bf-45ae-99cf-18f3c0138869.pdf"
query = f"Here is the link to the earnings report {url}"

r = model_with_tools.invoke(query)
