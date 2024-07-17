from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage

from helper.tools import scrape_info, answer
from llm.prompts import contextualize_q_prompt, qa_prompt
from helper.utils import setup_openai


setup_openai()


llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1)


tools = [scrape_info, answer]

class Earnest:
    def __init__(self):
        self.vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
        self._init_rag_chain()
        self.chat_history = []

    def _init_rag_chain(self):
        # Init rag chain
        retriever = self.vectorstore.as_retriever()
        self.llm_with_tools = llm.bind_tools(tools) 
        # Chain
        history_aware_retriever = create_history_aware_retriever(self.llm_with_tools, retriever, contextualize_q_prompt)
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def _assess_query(self, query: str):
        # Assess query
        msg = self.llm_with_tools.invoke(query)

        return msg
    
    def _process_user_input(self, human_message: str):
        msg = self._assess_query(human_message)
        if msg.tool_calls:
            query = msg.tool_calls[0]["args"]["query"]
            if msg.tool_calls[0]["name"] == "scrape_info":
                docs = scrape_info.run(query)
                self.enrich_knowledge_base(docs)
        # elif msg.tool_calls["name"] == "web_search":
        #     docs = web_search.run(query)
        #     self.enrich_knowledge_base(docs)

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

    def _check_knowledge_base(self, query: str):
        # Check knowledge base if info exists
        return self.vectorstore.similarity_search_with_relevance_scores(query)

    def enrich_knowledge_base(self, docs: Document):
        # Enrich the knowledge base with retrieved documents
        self.vectorstore.add_documents(documents=docs)

    def ask(self, user_input: str):
        msg = self._process_user_input(user_input)
        
        return msg
    
    def start(self, message: str):
        return self.ask(message)
