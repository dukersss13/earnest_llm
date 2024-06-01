from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.1)

prompt_template = \
"""
Your job is to help answer any questions related to the document retrieved. This document is the earnings report of a company.

If the user asks for a summary, give them the Total Net Revenue: <dollars> (Year over Year Percentage Change) [Page page_number],
Gross Profit: <dollars> (Year over Year % Change) [Page page_number],
Adjusted EBITDA: <dollars> (Year over Year % Change) [Page page_number],
Net Income: <dollars> (Year over Year % Change) [Page page_number],
Free Cash Flow: <dollars> (Year over Year Percentage Change) [Page page_number]

The context used to answer questions should only be related to the document retrieved.
If you do not know the answer, say you do not know.
Do not make things up. Be concise.

If you have an answer, put the page number containing this information in parentheses.

------------------------------

Here's an example:
<user_input>
<answer> (Page page_number)

------------------------------

{user_input}
{context}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["user_input"])
