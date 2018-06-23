# -*- coding: utf-8 -*-

from django.urls import path
from . import views
app_name = 'blog'
urlpatterns=[
        path('',views.IndexView.as_view(),name='index'),
        path('post/<int:post_pk>/',views.detail, name='detail'),#这他妈的只能用下划线吗post_pk
        path('archives/<int:year>/<int:month>/',views.Archives.as_view(),name='archives'),#传递的参数要在url里面
        path('category/<int:category_pk>/',views.CategoryView.as_view(),name='category'),
        ]


'''
        path('<int:question_id>/', views.detail, name='detail'),
        # ex: /polls/5/results/
        path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/5/vote/
        path('<int:question_id>/vote/', views.vote, name='vote'),
'''
