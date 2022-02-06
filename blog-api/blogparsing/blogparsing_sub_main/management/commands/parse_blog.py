from time import process_time_ns, strftime
from blogparsing_sub_main.models import BlogNews
import datetime
from datetime import datetime
from msilib.schema import Error
from turtle import title
import urllib.parse
from collections import namedtuple

import bs4
import requests

from django.core.management.base import BaseCommand

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from django.core.management.base import CommandError



InnerBlock = namedtuple('block', 'title,date,text,author,word_count')

class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.date}\t{self.text}\t{self.author}\t{self.word_count}'



class BlogParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0', 'Accept-Language': 'en'}


    def get_page(self, link):
        params = {
        }  

        r = self.session.get(link)
        r.raise_for_status()
        print(r)
        
        return r.text

    def get_links_of_archive(self):
        #сколько статей в блоге
        main_page = 'https://blog.python.org/'
        text = self.get_page(link=main_page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.find_all("a", {"class":"post-count-link"})
        # print(container)
        return container


    def parse_link(self, item):
        # Выбрать блок со ссылкой
        url_block = item
        
        # if not url_block:
        #     raise CommandError('bad "url_block" a')

        href = url_block.get('href')
        
        if href:
            url = 'https://pythoninsider.blogspot.com' + href
            print(1)
            
        else:
            url = None
            print(0)
        
        return href
        
    

    def parse_all(self):
        # Выбрать какое-нибудь задание
        links = self.get_links_of_archive()
        for item in links:
            url = self.parse_link(item=item)

            page_text = self.get_page(link=url)
            
            soup = bs4.BeautifulSoup(page_text, 'lxml')

            for item in soup.find_all("abbr", {"class": "published"}):
                print(item.get("title"))
                date = (item.get("title")[:10])
                
            for item in soup.find_all("h3", {"class": "post-title entry-title"}):
                title = item.text

            for item in soup.find_all("div", {"class": "post-body entry-content"}):
                text_body = item.text

                # 
                            
                stoplist = stopwords.words('english') # Bring in the default English NLTK stop words
                stoplist.extend([",", "@", ".", "!" "–", '(', ')', "’", ":", "|", "–", "%"])
                
                text_tokens = word_tokenize(text_body)

                tokens_without_sw = [word for word in text_tokens if not word in stoplist]
                word_count = len(tokens_without_sw)
                
                print(word_count)

                # 

            
            for item in soup.find_all("span", {"class": "fn"}):
                author = item.text


            p = BlogNews(
                title = title,
                date = date,
                author = author,
                text = text_body,
                word_count = word_count
            ).save()
            print(f'News {p}')

        return Block(
                title = title,
                date = date,
                author = author,
                text = text_body,
                word_count = word_count,
            )      
                
            
        
        # soup = bs4.BeautifulSoup(pagetext, 'lxml')

        # container = soup.find_all("div", {"class":"blog-posts hfeed"})

        
        

        # print(self.parse_link(self.get_links_of_archive()))

        # if not container:
        #     return 1
        # last_button = container[-1]
        # href = last_button.get('href')
        # if not href:
        #     return 1

        # r = urllib.parse.urlparse(href)
        # params = urllib.parse.parse_qs(r.query)
        # return min(int(params['p'][0]), self.PAGE_LIMIT)
        

# def main():
#     p = BlogParser()
#     p.parse_all()


# if __name__ == '__main__':
#     main()

class Command(BaseCommand):
    help = 'Парсинг blog.python.org'

    def handle(self, *args, **options):
        p = BlogParser()
        p.parse_all()