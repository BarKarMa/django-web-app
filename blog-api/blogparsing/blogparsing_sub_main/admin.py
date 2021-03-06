from django.contrib import admin

# Register your models here.
from .forms import NewsForm
from .models import BlogNews

@admin.register(BlogNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'date')
    form = NewsForm