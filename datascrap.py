import itertools
import requests
from bs4 import BeautifulSoup

def ScrapDev(urls):

    try:
        res = requests.get(urls).text.encode('utf8').decode('ascii', 'ignore')
        soup = BeautifulSoup(res, 'html.parser')
        find_title = soup.find_all("h2", class_="crayons-story__title")
        blogs={}
        for i in find_title:
            for x in  i.find_all("a", href=True, text=True):
                name=' '.join(i.text.strip().split())
                link=f"https://dev.to/{x['href']}"
                blogs[name]=link

        blog = itertools.islice(blogs.items(), 0, 5)
        return blog

    except Exception as e:
      print(e)
    