from app import app,api
from views import *

api.add_resource(SummariseNews,'/summarise-news')