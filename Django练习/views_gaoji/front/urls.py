from django.urls import path
from . import views

app_name = 'front'
urlpatterns = [
    path('add/', views.add_article, name='add'),
    path('list/', views.ArticleListView.as_view(), name='article_list')
]