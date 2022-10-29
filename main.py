from deta import Deta
import io
import os
import datetime
from datascrap import ScrapDev
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup
import json
from deta import app


load_dotenv(find_dotenv())

urls = os.environ.get("URL")
api_url = os.environ.get("APIURL")

project_key = os.environ.get("PROJECTKEY")
current_date = datetime.datetime.now()
folder_date=current_date.strftime("%x")
new_folder_date=folder_date.replace("/", "_")
deta = Deta(project_key)
blog = ScrapDev(urls)


@app.lib.run(action="apiblogs")
@app.lib.cron()
def blogs_scrapping(event):

    try:
        
        for key, value in blog:
            
            res=requests.get(str(value)).text.encode('utf8').decode('ascii', 'ignore')
            soup=BeautifulSoup(res, "html.parser")
            find_title=soup.find("h1")
            find_tags=soup.find("div", class_="spec__tags flex flex-wrap")
            find_article=soup.find("div", class_="crayons-article__main")
            title=' '.join(find_title.text.strip().split())
            tags=find_tags.text
            article=find_article.text
            article_tags=[x for x in tags.split()]


            new_article = str(find_article)

            data = {
                "title":title,
                "tags":article_tags,
                "body":new_article,
            }

            dumps_data = json.dumps(data)

            response = requests.post(api_url, json=data)
            print(response.text)
            if response.status_code =="400":
                continue

        return "Scrapped Successfully"

    except Exception as e: 
        print(e)

blogs_scrapping()