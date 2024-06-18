from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.tools.retriever import create_retriever_tool

from knowledge_base import KnowledgeBase
from utils import setup_openai

setup_openai()

llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.2)

prompt_template = \
"""
Your job is to give a summary of the document or help answer any questions related to the document retrieved.
This document is the earnings report of a company.

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

class Earnest:
    def __init__(self):
        self._init_rag_chain()

    def _init_rag_chain(self):
        # Init rag chain
        knowledge_base = KnowledgeBase()

        # Post-processing
        def format_docs(documents):
            return "\n\n".join(doc.page_content for doc in documents)

        retriever = knowledge_base.vectorstore.as_retriever()
        # Chain
        self.rag_chain = (
            {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    
    def ask(self, question: str):
        # 
        
        return self.rag_chain.invoke(question)
