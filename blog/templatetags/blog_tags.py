# -*- coding: utf-8 -*-

from ..models import Post,Category
from django import template
from django.db.models import Count#annotate的用法，计数，添加属性

register = template.Library()

@register.simple_tag#修饰器的作用，加入功能
def get_recent_posts(num=5):
    return Post.objects.all()[:num]
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    category_list = Category.objects.annotate(num_posts=Count('post'))#添加一个计数属性,QuerySet的方法中反向连接是直接用model的小写
    return category_list