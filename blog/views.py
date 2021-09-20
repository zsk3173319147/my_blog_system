import re
import markdown
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# 引入 Category 类
from .models import Post, Category,Tag
# Create your views here.

def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={
        'post_list':post_list
    })

def full_width(request):
    post_list=Post.objects.all().order_by('-created_time')
    return render(request,'full-width.html',context={
        'post_list':post_list
    })
    # return render(request,'full-width.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    md=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body=md.convert(post.body)
    # post.toc=md.toc

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''


    return render(request,'blog/detail.html',context={'post':post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
