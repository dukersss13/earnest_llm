# Earnest: Stocks Earnings Report AI Assistant

### Overview
As an avid investor in the stock market, I prefer to dabble in active investing and select my own stocks. I know... this is not the recommended way as to just dumping your money into the SP500 since it's been proven that the market will always outperform individual investing. With that said, I can't help myself to attempt to select my own companies to invest in and when I do, it's extremely important to keep up with these companies during their earnings seasons.

These earning reports tend to be extremely lengthy, often containing 100+ pages and not everything is completely relevant. With that said, Earnest was created as tool to help myself be more efficient when following earnings reports. Earnest is an Q&A AI assistant, powered by Chat-GPT or any other LLM of choice, aimed to **ONLY** help answer questions or provide a summary related to a given earnings document.

**DISCLAIMER:** Earnest's responses are NOT to be taken as financial or investment advice. It is simply just a Q&A chatbot. 


### Architecture Overview
Here is a high-level overview of how Earnest works.
Once the application is started, you will be taken to a window powered by Gradio interface.

You can proceed by providing Earnest a URL to the desired earnings report (PDF recommended). Earnest will know to scrape information from this document and store it in its vector database (Chroma).
Then, we are good to go and proceed with any questions you have. Earnest will have the complete chat history in its memory, so it will know exactly what was discussed.

![earnest_sketch](https://github.com/user-attachments/assets/f0b2fb79-02d7-43c6-9bda-e87a3df53825)


### Setup
To get started, you will need to install:

1. IDE of choice ([VSCode](https://code.visualstudio.com/download) recommended)
2. [Docker](https://www.docker.com/products/docker-desktop/) 
3. Generate [OpenAI API Key](https://openai.com/index/openai-api/) & store under **secrets/openai_api_key**
4. Generate [Tavily API Key](https://app.tavily.com/home) & store under **secrets/tavily_api_key**
5. Generate [Google Search API Key](https://python.langchain.com/v0.2/docs/integrations/tools/google_search/) (Optional) & store under **secrets/google_cse and secrets/google_api_key**

Once all the steps are done, open the application in a Docker dev-container. The best thing about Docker containers is that it will allow the application to work out of the box, without having to re-install dependencies.

Finally, go ahead and click run on **main.py** or run **python3 main.py** in your terminal and enjoy!


### Future Work
1. Better UI
2. Enable Web Search
