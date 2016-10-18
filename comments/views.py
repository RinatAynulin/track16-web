from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from .models import Comment

def index(request):
    latest_comments_list = Comment.objects.order_by('created_at')[:10]
    template = loader.get_template('comments/index.html')
    context = {
        'latest_comments_list' : latest_comments_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist")
    template = loader.get_template('comments/detail.html')
    context = {
        'comment' : comment,
    }
    return HttpResponse(template.render(context, request))
