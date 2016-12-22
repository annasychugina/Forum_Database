from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create),
    url(r'^details/$', views.details),
    url(r'^listPosts/$', views.listPosts),
    url(r'^listThreads/$', views.listThreads),
    url(r'^listUsers/$', views.listUsers),
]