from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from blogparsing_sub_main.models import BlogNews

from collections import namedtuple
from collections import Counter

import bs4
import requests

from django.core.management.base import BaseCommand

import nltk
nltk.download('stopwords')
nltk.download('punkt')


InnerBlock = namedtuple('block', 'title,date,text,author,word_count,top_words')


class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.date}\t{self.text}\t{self.author}\t{self.word_count}\t{self.top_words}'


class BlogParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0', 'Accept-Language': 'en'}

    def get_page(self, link):
        r = self.session.get(link)
        r.raise_for_status()
        print(r)
        return r.text

    def get_links_of_archive(self):
        # сколько статей в блоге
        main_page = 'https://blog.python.org/'
        text = self.get_page(link=main_page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.find_all("a", {"class": "post-count-link"})
        return container

    def parse_link(self, item):
        # Выбрать блок со ссылкой
        url_block = item

        href = url_block.get('href')

        if href:
            url = 'https://pythoninsider.blogspot.com' + href
        else:
            url = None
        return href

    def parse_all(self):
        count = 0
        # Выбрать какое-нибудь задание
        links = self.get_links_of_archive()
        for item in links:
            count = count+1
            print(count)
            url = self.parse_link(item=item)

            page_text = self.get_page(link=url)

            soup = bs4.BeautifulSoup(page_text, 'lxml')

            for item in soup.find_all("abbr", {"class": "published"}):
                date = (item.get("title")[:10])
                print(date)

            for item in soup.find_all("h3", {"class": "post-title entry-title"}):
                title = item.text
            # получения значений текста статей
            for item in soup.find_all("div", {"class": "post-body entry-content"}):
                # текст статьи
                text_body = item.text

                # добавление в стандарнтые стоп слова и пунктуацию новых исходя из текстов статей
                # Bring in the default English NLTK stop words
                stoplist = stopwords.words('english')
                stoplist.extend([",", "@", ".", "!", "–", '(', ')',
                                "’", ":", "|", "–", "%", "The", "*", '“', '”', '?'])

                text_tokens = word_tokenize(text_body)

                # убираем стоп слова и пунктуацию
                tokens_without_sw = [
                    word for word in text_tokens if not word in stoplist]
                word_count = len(tokens_without_sw)

                top_words = [i[0] for i in Counter(
                    " ".join(tokens_without_sw).split()).most_common(10)]
                converted = ' '.join([str(elem) for elem in top_words])

            for item in soup.find_all("span", {"class": "fn"}):
                author = item.text

            p = BlogNews(
                title=title,
                date=date,
                author=author,
                text=text_body,
                word_count=word_count,
                top_words=converted,
            ).save()

        return Block(
            title=title,
            date=date,
            author=author,
            text=text_body,
            word_count=word_count,
            top_words=converted,
        )

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
