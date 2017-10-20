from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_list, name="news_list"),
    url(r'^(?P<site>[\W\w]+)/news/$', views.news_list, name="news_list_based_site"),
]