
from django.shortcuts import render
from .dashboard_logic.all_years_top_5 import Filtering


# Create index function to display the HTML file into the browser
def index(request):
    if not request.GET or (request.GET['years']=='all years'):
        choosen_year = 'all years'
        filter_result = Filtering().filter_all_years(request=request)
    else:
        choosen_year = request.GET.get('years')
        filter_result= Filtering().filter_all_years(request=request, choosen_year=choosen_year)

    context = { 
            'data': filter_result.top_5_all,
            'avg': filter_result.count_words_avg,
            'top_words': filter_result.top_words,
            'choosen_year':choosen_year,
            'all_times_avg':filter_result.all_times_avg

         
    }
    return render(request, "index.html", context)