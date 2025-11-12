from flask_restful import Resource
from utils import *

class SummariseNews(Resource):
    def get(self):
        top_news_list = get_top_news()

        summary_of_content = summarise_with_gemini(data=top_news_list)

        return summary_of_content