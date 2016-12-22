from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create),
    url(r'^details/$', views.details),
    url(r'^list/$', views.list),
    url(r'^remove/$', views.remove),
    url(r'^restore/$', views.restore),
    url(r'^update/$', views.update),
    url(r'^vote/$', views.vote),
]