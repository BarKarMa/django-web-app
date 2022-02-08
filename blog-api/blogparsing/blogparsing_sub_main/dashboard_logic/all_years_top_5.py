from blogparsing_sub_main.models import BlogNews
from django.db.models import Count
from collections import namedtuple
from ..models import Round
from django.db.models import Avg
from django.db.models import IntegerField
from collections import Counter

InnerBlock = namedtuple('block', 'top_5_all,top_words,count_words_avg,all_times_avg')

class BlockFilter(InnerBlock):
    def __str__(self):
        return f'{self.top_5_all}\t{self.top_words}\t{self.count_words_avg}\t{self.all_times_avg}\t'


class Filtering():
    def filter_all_years(self, request, choosen_year=all):
        all_times_avg =BlogNews.objects.values("date__year")\
                .annotate(word_count__avg=Round(Avg('word_count', output_field=IntegerField()))).aggregate(final=Round(Avg('word_count__avg',output_field=IntegerField())))
            
        if not request.GET or (request.GET['years']=='all years'):
            # Топ-5 за все время
            top_5_all = BlogNews.objects.values("author")\
                        .annotate(total=Count('author'))\
                        .order_by('total').reverse()[:5] 
            # топ-10 слов за все время
            top_words = BlogNews.objects.values("top_words")
            converted_words_to_all = (' '.join([str(elem['top_words']) for elem in top_words]))
            top_words = [i[0] for i in Counter(" ".join(converted_words_to_all.split()).split()).most_common(10)]

            # среднее колличество слов за все время
            count_words_avg = BlogNews.objects.values("date__year")\
                               .annotate(word_count__avg=Round(Avg('word_count', output_field=IntegerField())))
             
            
        else:
            # Топ-5 по годам
            top_5_all = BlogNews.objects.values("author", "date__year")\
                        .filter(date__year=choosen_year) \
                        .annotate(total=Count('author')) \
                        .order_by('total').reverse()[:5]
            # топ 10 слов при фильтрации по годам
            top_words = BlogNews.objects.values("top_words")\
                        .filter(date__year=choosen_year)
            converted_words_to_all = (' '.join([str(elem['top_words']) for elem in top_words]))
            top_words = [i[0] for i in Counter(" ".join(converted_words_to_all.split()).split()).most_common(10)]

            # среднее колличество слов по годам
            count_words_avg = BlogNews.objects.values("date__year")\
                .filter(date__year=choosen_year)\
                .annotate(word_count__avg=Round(Avg('word_count', output_field=IntegerField())))
            
        

        return BlockFilter(
            top_5_all=top_5_all,
            top_words=top_words,
            count_words_avg=count_words_avg,
            all_times_avg=all_times_avg,
        )

