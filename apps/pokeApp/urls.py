from django.conf.urls import include, url
from django.contrib import admin
from . import views

app_name = 'poke'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^pokes/$', views.pokes, name="pokes"),
    url(r'^pokes/(?P<userId>[0-9]+)/$', views.pokeUser, name="pokeUser")   
]