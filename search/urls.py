from django.urls import path

from search.views import *

app_name = "search"

urlpatterns = [
    path('',SearchView.as_view(),name="search"),
    path('add/',add_feature,name="add"),
    path('songs/<str:artist_name>/',SongView.as_view(),name="songlist"),
    path('match/',match,name="match"),
    path('hello/',hello_world,name='hello_world')
]