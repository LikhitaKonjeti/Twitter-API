from django.conf.urls import url
from . import views

urlpatterns= [
    # /music/
    url(r'^$',views.index,name='index'),
    url(r'^search/$',views.search,name='search'),
    url(r'^search/filter/$',views.filter,name='filter'),
    ]
