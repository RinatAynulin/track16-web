from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from .models import Post

def index(request):
    latest_posts_list = Post.objects.order_by('-created_at')
    template = loader.get_template('posts/index.html')
    context = {
        'latest_posts_list' : latest_posts_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    template = loader.get_template('posts/detail.html')
    context = {
        'post' : post,
    }
    return HttpResponse(template.render(context, request))
