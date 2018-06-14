from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post_list/', views.post_list, name='post_list'),
    url(r'^$', views.main_site, name='main_site'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail')
]
