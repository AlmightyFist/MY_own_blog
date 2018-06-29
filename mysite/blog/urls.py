from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('', views.main_site, name='main_site'),
    path('post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/$', views.post_new, name ='post_new'),
    path('post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path('(?P<pk>\d+)/share/$', views.post_share,name='post_share'),
]
"""urlpatterns = [
    url(r'^post_list/', views.PostListView.as_view(), name='post_list'),
    url(r'^$', views.main_site, name='main_site'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name ='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<pk>\d+)/share/$', views.post_share,name='post_share'),
]"""
