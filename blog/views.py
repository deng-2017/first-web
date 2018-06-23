# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
# Create your views here.
from django.http import HttpResponse
from .models import Post,Category
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView



def detail(request,post_pk):
    
    post1=Post.objects.annotate(comment_num=Count('comment'))####注意理解！！！！！！！！！！！！！！！！！！！！！！！！
    post = get_object_or_404(post1, pk=post_pk)###注意理解！！！！！！！！！！！！！
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)
#注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
#其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
    

#在模板中找到展示博客文章主体的 {{ post.body }} 部分，为其加上 safe 过滤器，{{ post.body|safe }}，大功告成，这下看到预期效果了。
#safe 是 Django 模板系统中的过滤器（Filter），可以简单地把它看成是一种函数，其作用是作用于模板变量，将模板变量的值变为经过滤器处理过后的值。
#例如这里 {{ post.body|safe }}，本来 {{ post.body }} 经模板系统渲染后应该显示 body 本身的值，但是在后面加上 safe 过滤器后，
#渲染的值不再是body 本身的值，而是由 safe 函数处理后返回的值。过滤器的用法是在模板变量后加一个 | 管道符号，再加上过滤器的名称。
#可以连续使用多个过滤器，例如 {{ var|filter1|filter2 }}。
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(Archives,self).get_queryset().filter(created_time__year=year,created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate=get_object_or_404(Category,self.kwargs.get('category_pk'))
        return super(Category,self).get_queryset().filter(category=cate)#理解self.kwaargs.get，还有super 父类继承，还有get_
    #queryset()调用和复写。

