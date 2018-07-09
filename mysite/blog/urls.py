from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    path('', views.main_site, name='main_site'),
    path('post/(?P<int:pk>\d+)/$', views.post_detail, name='post_detail'),
    path('post/new/$', views.post_new, name ='post_new'),
    path('post/(?P<int:pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path('/(?P<int:pk>\d+)/share/$', views.post_share,name='post_share'),
    path('post/(?P<int:pk>\d+)/vote/$', views.vote, name='post_vote'),
    path('post/(?P<int:pk>\d+)/add_comment/$',views.add_comment, name='add_comment'),
    path('tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag')
]
"""urlpatterns = [
    url(r'^post_list/', views.PostListView.as_view(), name='post_list'),
    url(r'^$', views.main_site, name='main_site'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name ='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<pk>\d+)/share/$', views.post_share,name='post_share'),
]"""
