import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from newsapi import NewsApiClient
import time
import openai

# Read API keys from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]
newsapi_key = st.secrets["newsapi_key"]

# Initialize OpenAI API
openai.api_key = openai_api_key

# Define Prompt Template
template = """
You are an AI assistant helping an equity research analyst. Given the following query and the provided news article summaries, provide an overall summary.

Query: {query}
Summaries: {summaries}
"""

prompt = PromptTemplate(template=template, input_variables=['query', 'summaries'])
llm_chain = LLMChain(prompt=prompt, llm=OpenAI(api_key=openai_api_key))

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=newsapi_key)

def get_news_articles(query):
    try:
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        return articles['articles']
    except Exception as e:
        return {'error': str(e)}

def summarize_articles(articles):
    summaries = []
    for article in articles:
        description = article.get('description')
        if description:
            summaries.append(description)
    return ' '.join(summaries)

def get_summary(query):
    articles = get_news_articles(query)
    if 'error' in articles:
        return articles['error']
    summary = summarize_articles(articles)
    return summary

def call_openai_with_rate_limit_handling(prompt):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except openai.error.RateLimitError:
        st.error("Rate limit exceeded. Retrying after 60 seconds.")
        time.sleep(60)
        return call_openai_with_rate_limit_handling(prompt)
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
        return "An error occurred while processing your request."

