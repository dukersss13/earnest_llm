# Earnest: Stocks Earnings Report Q&A Chatbot

### Overview
As an avid investor in the stock market, I prefer to dabble in active investing and select my own stocks. I know... this is not the recommended way as to just dumping your money into the S&P500 since it's been proven that the market will always outperform individual investing. With that said, I can't help myself to attempt to select my own companies to invest in and when I do, it's extremely important to keep up with these companies during their earnings seasons.

These earning reports tend to be extremely lengthy, often containing 100+ pages and not everything is completely relevant. With that said, Earnest was created as tool to help myself be more efficient when following earnings reports. Earnest is an Q&A AI assistant, powered by Chat-GPT or any other LLM of choice, aimed to **ONLY** help answer questions or provide a summary related to a given earnings document.

**DISCLAIMER:** Earnest's responses are NOT to be taken as financial or investment advice. It is simply just a Q&A chatbot. 


### Architecture Overview
Here is a high-level overview of how Earnest works.
Once the application is started, you will be taken to an interface powered by Gradio.

You can proceed by providing Earnest a URL to the desired earnings report (PDF recommended). Earnest will know to scrape information from this document and store it in its vector database (Chroma).
If you don't have an URL at hand, you can also instruct Earnest to do a web search for any earnings reports. Then, we are good to go and proceed with any questions you have. Earnest will have the complete chat history in its memory, so it will know exactly what was discussed.


![Screenshot 2024-11-08 at 2 34 27 PM](https://github.com/user-attachments/assets/e2c912e4-159a-4534-9d83-ad4d45090bae)


![image](https://github.com/user-attachments/assets/54691842-9da0-4ae5-82c3-350f8253da72)




### Setup
To get started, you will need to install:

1. IDE of choice ([VSCode](https://code.visualstudio.com/download) recommended)
2. [Docker](https://www.docker.com/products/docker-desktop/) 
3. Generate [OpenAI API Key](https://openai.com/index/openai-api/) & store under **secrets/openai_api_key**
4. Generate [Tavily API Key](https://app.tavily.com/home) & store under **secrets/tavily_api_key**
5. Generate [Google Search API Key](https://python.langchain.com/v0.2/docs/integrations/tools/google_search/) (Optional) & store under **secrets/google_cse and secrets/google_api_key**

Once all the steps are done, open the application in a Docker dev-container. The best thing about Docker containers is that it will allow the application to work out of the box, without having to re-install dependencies.

Finally, go ahead and click run on `main.py` or run `python3 main.py` in your terminal and enjoy!

### Earnest in Action
Start by providing the link to your desired document and Earnest can start answering or retrieve any key information related to the document immediately. Earnest was also prompted to provide the pages the information is retrieved from so you can double check the information provided. This is served as guardrails against LLM hallucination.

![image](https://github.com/user-attachments/assets/c6082b79-9fe3-4700-8e14-5e6c581d7234)

![Screenshot 2024-07-19 at 1 39 33 PM](https://github.com/user-attachments/assets/ef9609b7-e202-45d0-bedb-f2a3346e1338)

### Future Work
1. Better UI
2. Optimize RAG Speed
