from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from newsapi import NewsApiClient
from unittest.mock import patch

# Mock OpenAI Initialization and Calls
class MockOpenAI:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return "Mocked summary response."

# Mock NewsApiClient Initialization and Method
class MockNewsApiClient:
    def __init__(self, *args, **kwargs):
        pass

    def get_everything(self, *args, **kwargs):
        return {
            'articles': [
                {'description': 'Article 1 description.'},
                {'description': 'Article 2 description.'},
                {'description': None},  # Simulate None description
                {'description': 'Article 4 description.'}
            ]
        }

# Patching the OpenAI and NewsApiClient classes
with patch('langchain_openai.OpenAI', MockOpenAI), patch('newsapi.NewsApiClient', MockNewsApiClient):
    openai_api_key = 'sk-proj-jsFXcInKfwMto5JHf8pXT3BlbkFJrbQz7T6IE0GJ1ex6wuN9'
    openai = OpenAI(api_key=openai_api_key)

    newsapi = NewsApiClient(api_key='07ddff56fdb1407caf7d1075d16326fc')

    def get_news_articles(query):
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        return articles['articles']

    def summarize_articles(articles):
        summaries = []
        for article in articles:
            description = article.get('description')
            if description is None:
                description = 'No description available.'
            summaries.append(description)
        return ' '.join(summaries)

    def get_summary(query):
        articles = get_news_articles(query)
        summary = summarize_articles(articles)
        return summary

    template = """
    You are an AI assistant helping an equity research analyst. Given the following query and the provided news article summaries, provide an overall summary.

    Query: {query}
    Summaries: {summaries}
    """

    prompt = PromptTemplate(template=template, input_variables=['query', 'summaries'])

    class MockRunnableSequence:
        def __init__(self, *args, **kwargs):
            pass
        
        def run(self, *args, **kwargs):
            return "Mocked summary response."
    
    llm_chain = MockRunnableSequence(prompt | openai)

    # Example usage
    query = "latest trends in artificial intelligence"
    article_summaries = get_summary(query)
    summary_input = {'query': query, 'summaries': article_summaries}
    summary = llm_chain.run(summary_input)
    print(summary)
