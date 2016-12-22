from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create),
    url(r'^details/$', views.details),
    url(r'^list/$', views.list),
    url(r'^listPosts/$', views.listPosts),
    url(r'^remove/$', views.remove),
    url(r'^restore/$', views.restore),
    url(r'^close/$', views.close),
    url(r'^open/$', views.open),
    url(r'^update/$', views.update),
    url(r'^vote/$', views.vote),
    url(r'^subscribe/$', views.subscribe),
    url(r'^unsubscribe/$', views.unsubscribe),
]