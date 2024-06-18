from utils import setup_openai
from earnest import llm, prompt
from langchain_core.messages import HumanMessage
from web_search import *


setup_openai()

# tools = [conduct_websearch]

# from langchain.agents import create_tool_calling_agent

# model_with_tools = llm.bind_tools(tools)

# request = "Search for Tesla Q4 2023 earnings report 10-k"

# r = model_with_tools.invoke([HumanMessage(content=request)])
