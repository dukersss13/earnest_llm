from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def craft_prompt(prompt: str) -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
    return prompt


### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = craft_prompt(contextualize_q_system_prompt)


### Answer question ###
system_prompt = (
    """
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer
    the question. If you don't know the answer, say that you
    don't know.
    {context}
    After the user provides the proper information, ask them if they have any questions related to the document.
    If the user asks for a summary, summarize it in a paragraph and include all the key financial metrics such as:
    total net revenue, net income, gross profit, adjusted EBITDA, net loss, cash flow.
    If you have an answer, put the page number containing this information in parentheses.

    ------------------------------
    Here's an example:

    User: Hi
    Answer: Hello, please provide a URL to the earnings report
    User: 'fakeeraningsreport.com/10340.pdf'
    Answer: What questions can I answer for you regarding this earnings report?
    User: What is the company's total net revenue?
    Answer:  The total net revenue was $100M (Page <page_number>)
    """
)
qa_prompt = craft_prompt(system_prompt)
