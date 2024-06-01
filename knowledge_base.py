from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

from earnest import prompt, llm


# Load Documents
url = "https://s27.q4cdn.com/749715820/files/doc_financials/2023/q4/a31f2915-31bf-45ae-99cf-18f3c0138869.pdf"
loader = PyPDFLoader(url)
pages = loader.load_and_split()

# Embedding
vectorstore = Chroma.from_documents(documents=pages, 
                                    embedding=OpenAIEmbeddings())

# Retriever
retriever = vectorstore.as_retriever()


# Post-processing
def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

# Chain
rag_chain = (
    {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
