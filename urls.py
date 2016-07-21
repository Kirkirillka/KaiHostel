__author__ = 'kirill'


from django.conf.urls import url
from KaiHostel3.views import *

app_name="KaiHostel3"

urlpatterns=[
    url(r'^$',index),
    url(r'login/$',Login.as_view(),name='login'),
    url(r'logout/$',Logout.as_view(),name='logout'),
    url(r'add_article/$',AddArticle.as_view(),name='add_article'),
    url(r'articles/?page=(?P<page>[0-9]+)/$',AllArticle.as_view(),name='all_article'),
    url(r'detail_article/(?P<pk>[0-9]+)/$',GetArticle.as_view(),name='detail_article'),
    url(r'register/$',Register.as_view(),name='register'),
    url(r'add_comment/$',AddComment.as_view(),name='add_comment'),
    url(r'all_comment/$',AllComment.as_view(),name='all_comment'),
    url(r'del_comment/(?P<article_id>[0-9]+)/$',DeleteArticle.as_view(),name='del_article')
]