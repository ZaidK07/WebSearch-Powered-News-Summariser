from google import genai
import os
import requests
import json

GEMINI_API_KEY = os.getenv("GENAI_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

GC_CLIENT = genai.Client(api_key = GEMINI_API_KEY)
GC_MODEL = "gemini-2.5-flash"

NEWS_TOPICS = os.getenv("NEWS_TOPICS").split(',')
base_url = "https://www.googleapis.com/customsearch/v1"
pages = 1
system_instruction_prompt = """You are a summariser assistant.
You will be provided with list of news of user's intrest your job is to summarise them and present them to user in such a way so that no important detail is lost from news and no fluff goes to user.
Strictly give response with enough detailed summary that user does not miss out on something but also not long like an essay.
"""


def perform_search(page_no,search_query):
    params = {
        'key': SEARCH_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': search_query,
        # 'num': 1, # NOTE: this is only for testing phase comment this line afterwards
        'page': page_no
    }
    search_json = requests.get(base_url,params=params).json()
    search_data = search_json.get("items",[])
    search_data_dict_list = []
    for search_item in search_data:
        search_data_dict_list.append({
            'link': search_item['link'],
            'title': search_item['title'],
            'snippet': search_item['snippet']
        })
    return {'page_no': page_no, 'page_content': search_data_dict_list}


def get_top_news():
    top_news_list = []
    for news_topic in NEWS_TOPICS:
        per_topic_list = []
        for page_no in range(1, pages+1):
            search_query = f'Latest news regarding {news_topic}'
            search_data = perform_search(page_no=page_no,search_query=search_query)
            per_topic_list.append(search_data)
        top_news_list.append({
            'topic': news_topic,
            'content': per_topic_list
        })
    return top_news_list


def summarise_with_gemini(data):
    response = GC_CLIENT.models.generate_content(
        model = GC_MODEL,
        contents = json.dumps(data),
        config = genai.types.GenerateContentConfig(
        system_instruction=system_instruction_prompt
        )
    )
    return response.text