from django.urls import path
# Импортируем созданное нами представление
from .views import (NewsList, NewsDetail, NewsListSearch, PostCreate, PostUpdate,
                    PostDelete, PostCreateAR, PostUpdateAR, PostDeleteAR)
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем статьям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*1)(NewsList.as_view()), name='all_news'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewsDetail.as_view(), name='detail_one_news'),
   path('search', NewsListSearch.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/news/edit/', PostUpdate.as_view(), name='news_create'),
   path('<int:pk>/news/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreateAR.as_view(), name='articles_create'),
   path('<int:pk>/articles/edit/', PostUpdateAR.as_view(), name='articles_create'),
   path('<int:pk>/articles/delete/', PostDeleteAR.as_view(), name='articles_delete'),

]