import numpy as np

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage

from helper.config import MODEL
from helper.tools import find_urls, scrape_info, web_search
from llm.prompts import contextualize_q_prompt, qa_prompt
from helper.utils import setup_openai


setup_openai()


llm = ChatOpenAI(model_name=MODEL, temperature=0.2)


class Earnest:
    def __init__(self):
        self.vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
        self._init_rag_chain()
        self.chat_history = []

    def _init_rag_chain(self):
        # Init rag chain
        retriever = self.vectorstore.as_retriever()
        # Chain
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def _assess_query(self, query: str):
        # Assess query
        urls = find_urls(query)
        if len(urls):
            docs = scrape_info(urls)
            self._enrich_knowledge_base(docs)
        elif "look up" in query.lower() or "search" in query.lower() or self._check_knowledge_base(query):
            docs = web_search(query)
            self._enrich_knowledge_base(docs)
    
    def _process_user_input(self, human_message: str) -> str:
        """
        Process user input

        :param human_message: human message
        :return: LLM output
        """
        self._assess_query(human_message)
        llm_output = self.rag_chain.invoke({"input": human_message, "chat_history": self.chat_history})
        llm_message = llm_output["answer"]
        self._update_chat_history(human_message, llm_message)

        return llm_message

    def _update_chat_history(self, human_message: str,
                             llm_message: str):
        """
        Update the chat history
        """
        self.chat_history.extend(
            [
                HumanMessage(content=human_message),
                AIMessage(content=llm_message)
            ]
        )

    def _check_knowledge_base(self, query: str) -> bool:
        # Check knowledge base if info exists
        result_with_scores = self.vectorstore.similarity_search_with_score(query)

        return np.all([doc[1] < 0.3 for doc in result_with_scores])

    def _enrich_knowledge_base(self, docs: Document):
        # Enrich the knowledge base with retrieved documents
        self.vectorstore.add_documents(documents=docs)

    def ask(self, user_input: str):
        msg = self._process_user_input(user_input)
        
        return msg
