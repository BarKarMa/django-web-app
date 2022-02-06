from django.db import models

# Create your models here.

class BlogNews(models.Model):
    title = models.TextField(verbose_name='title',
    )

    date = models.DateField(verbose_name='date',
    )

    text = models.TextField(verbose_name='text',
    ) 

    author = models.TextField(verbose_name='author',
    )
    word_count = models.IntegerField(verbose_name='word_count', default=0,
    )