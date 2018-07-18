from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.views import login, logout, logout_then_login
from django.contrib.auth.views import password_change, password_change_done, password_reset, password_reset_done
from django.contrib.auth.views import password_reset_confirm, password_reset_complete

urlpatterns = [
    #Adresu URL logowania i wylogowania
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout_then_login',logout_then_login, name='logout_then_login'),
    #Adres URL rejestracji użytkownika
    path('register/',views.register, name='register'),
    #Adresy URL do obsługi haseł
    path('password_change/', password_change, name='password_change' ),
    path('password_change/done',password_change_done, name='password_change_done'),
    path('password_reset/',password_reset, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',password_reset_confirm,name='password_reset_confirm'),
    path('password_reset/complete/', password_reset_complete, name='password_reset_complete'),
    #Adresy URL obsługi strony
    path('post_list/', views.post_list, name='post_list'),
    path('', views.main_site, name='main_site'),
    path('post/(?P<int:pk>\d+)/$', views.post_detail, name='post_detail'),
    path('post/new/$', views.post_new, name ='post_new'),
    path('post/(?P<int:pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    path('/(?P<int:pk>\d+)/share/$', views.post_share,name='post_share'),
    path('post/(?P<int:pk>\d+)/vote/$', views.vote, name='post_vote'),
    path('post/(?P<int:pk>\d+)/add_comment/$',views.add_comment, name='add_comment'),
    path('tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    path('category/(?P<int:pk>\d+)/$', views.category_posts, name ='category_posts'),
]
"""urlpatterns = [
    url(r'^post_list/', views.PostListView.as_view(), name='post_list'),
    url(r'^$', views.main_site, name='main_site'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name ='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<pk>\d+)/share/$', views.post_share,name='post_share'),
]"""
