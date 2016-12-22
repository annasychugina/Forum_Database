from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create),
    url(r'^details/$', views.details),
    url(r'^follow/$', views.follow),
    url(r'^unfollow/$', views.unfollow),
    url(r'^listPosts/$', views.listPosts),
    url(r'^updateProfile/$', views.updateProfile),
    url(r'^listFollowers/$', views.listFollowers),
    url(r'^listFollowing/$', views.listFollowing),
]