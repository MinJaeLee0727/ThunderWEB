from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    # ex: /search/
    path('', views.index, name='search_index'),
    # ex: /search/results/?SummonerName=KR_Kritic/
    path('results/', views.results, name='results'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]