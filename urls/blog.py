from django.conf.urls import patterns, include, url
from django.contrib import admin
import urls
from apps.blog import views

urlpatterns = patterns('',
    url(r'^(?P<pk>[\w\d]+)/(?P<slug>[\w\d-]+)/$', views.PostDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[\w\d]+)/(?P<slug>[\w\d-]+)/edit/$', views.PostUpdate.as_view(), name='update'),
    url(r'^(?P<pk>[\w\d]+)/(?P<slug>[\w\d-]+)/delete/$', views.PostDelete.as_view(), name='delete'),
    url(r'^add/$', views.PostCreate.as_view(), name='post_create'),
    url(r'^post_list', views.PostList.as_view(), name='post_list'),
    url(r'^search', views.Example.as_view(), name='post_search'),
)
