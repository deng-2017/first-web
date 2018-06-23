# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
# Create your views here.
from django.http import HttpResponse
from .models import Post,Category
import markdown
from comments.forms import CommentForm

from django.views.generic import ListView, DetailView
'''
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
    return render(request,'blog/detail.html', context=context)
#注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
#其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
    

#在模板中找到展示博客文章主体的 {{ post.body }} 部分，为其加上 safe 过滤器，{{ post.body|safe }}，大功告成，这下看到预期效果了。
#safe 是 Django 模板系统中的过滤器（Filter），可以简单地把它看成是一种函数，其作用是作用于模板变量，将模板变量的值变为经过滤器处理过后的值。
#例如这里 {{ post.body|safe }}，本来 {{ post.body }} 经模板系统渲染后应该显示 body 本身的值，但是在后面加上 safe 过滤器后，
#渲染的值不再是body 本身的值，而是由 safe 函数处理后返回的值。过滤器的用法是在模板变量后加一个 | 管道符号，再加上过滤器的名称。
#可以连续使用多个过滤器，例如 {{ var|filter1|filter2 }}。
'''
# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg ='post_pk'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
       

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        
        post = super(PostDetailView, self).get_object(queryset=None)
        
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context



class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
       #return super().get_queryset().annotate(comment_num=Count('comment'))
       return Post.objects.annotate(comment_num=Count('comment'))####这里要理解下get_queryset是一定会执行的，应该是在as.view()立面

class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(Archives,self).get_queryset().filter(created_time__year=year,created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate=get_object_or_404(Category,self.kwargs.get('category_pk'))
        return super(Category,self).get_queryset().filter(category=cate)#理解self.kwargs.get，还有super 父类继承，还有get_
    #queryset()调用和复写。
