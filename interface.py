from llm.earnest import Earnest
import gradio as gr


earnest = Earnest()

def predict(message, history):
    response = earnest.ask(message)

    return response

interface = gr.ChatInterface(predict)
