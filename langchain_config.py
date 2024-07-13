from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from newsapi import NewsApiClient

# Initialize OpenAI API
openai_api_key = 'sk-proj-FsWNF91GJItVdVZfkuVAT3BlbkFJsdYKmR5GYJRosUvO63aG'  
openai = OpenAI(api_key=openai_api_key)

# Define Prompt Template
template = """
You are an AI assistant helping an equity research analyst. Given the following query and the provided news article summaries, provide an overall summary.

Query: {query}
Summaries: {summaries}
"""

prompt = PromptTemplate(template=template, input_variables=['query', 'summaries'])
llm_chain = LLMChain(prompt=prompt, llm=openai)

# Initialize NewsAPI
newsapi_key = "07ddff56fdb1407caf7d1075d16326fc"  
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
