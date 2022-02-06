import datetime
from datetime import datetime
from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.db.models import Count
from blogparsing_sub_main.models import BlogNews
from django.db.models import Sum, Avg
from django.db.models.functions import  Lower, Length

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter

# Create your views here.

# Create index function to display the HTML file into the browser
def index(request):
    choosen_year = request.GET.get('years', False)
    if not choosen_year:
         choosen_year=2022
    data = BlogNews.objects.all()
    # for item in data:
        # text = len(item.text.split())
        # da = item.date.strftime("%Y")

    
    #  топ 5 авторов по колличеству постов по годам переменная передается со страници
    top_5_by_years = BlogNews.objects.values("date__year","author").annotate(total=Count('author')).filter(date__year=choosen_year)

    #  топ 5 авторов по колличеству постов за все время
    top_5_all = BlogNews.objects.values("author").annotate(total=Count('author'))[:5]
    
    

    data = BlogNews.objects.values("date__year").filter(date__year=choosen_year).annotate(Avg('word_count'))

    print(data)
    # for item in data:
        
    #     print(item)


    
    
    # top_10 = Counter(text_al[1]).most_common(10)

    
    
    # print(round(avg,2))


    context = {
            'data': top_5_all,
            'top_by_years': top_5_by_years,
            'avg': data

            
    }
    return render(request, "index.html", context)