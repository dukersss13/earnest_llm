import re
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

from knowledge_base import KnowledgeBase, RequestType
from utils import setup_openai

setup_openai()

llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.2)

system_prompt = \
"""
Start by asking the user if they have a specific company and quarterly earnings
report they want to research. Tell the user you can also accept PDF urls of the earnings report.

Your job is to give a summary of the document or help answer any questions related to the document retrieved.
This document is the earnings report of a company.

If the user asks for a summary, summarize it in a paragraph and include all the key metrics.

The context used to answer questions should only be related to the document retrieved.
If you cannot answer the question, ask the user to rephrase the question or be more specific.
Do not make things up. Be concise.

If you have an answer, put the page number containing this information in parentheses.

------------------------------
<context>

Here's an example:
What is the total net revenue?
The total net revenue was $100M (Page <page_number>)

------------------------------

{user_input}
{context}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{user_input}"),
    ]
)

# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)


class Earnest:
    def __init__(self):
        self._init_rag_chain()

    def _init_rag_chain(self):
        # Init rag chain
        self.knowledge_base = KnowledgeBase()

        # Post-processing
        def format_docs(documents: list[Document]):
            return "\n\n".join(doc.page_content for doc in documents)

        retriever = self.knowledge_base.vectorstore.as_retriever()
        # Chain
        self.rag_chain = (
            {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
            | prompt
            | llm.bind_tools([self.knowledge_base.scrape_info,
                              self.knowledge_base.web_search])
            | StrOutputParser()
        )

    def _assess_query(self, query: str) -> tuple[RequestType, str]:
        # Assess the query from the user
        urls = Earnest._find_urls(query)
        if urls:
            query = (RequestType.SCRAPE, urls)
        else:
            query = (RequestType.SEARCH, query)

        return query

    def _check_knowledge_base(self, query: str):
        # Check knowledge base if info exists
        return self.knowledge_base.vectorstore.similarity_search_with_relevance_scores(query)
    
    def ask(self, query: str):
        # First check Knowledge Base if info exists
        # if not self._check_knowledge_base(query):
        #     query_tuple = self._assess_query(query)
        #     self.knowledge_base.enrich_knowledge_base(query_tuple)

        return self.rag_chain.invoke(query)

    def start(self):
        # Kickstart Earnest
        starting_input = "Hi"
        return self.rag_chain.invoke(starting_input)

