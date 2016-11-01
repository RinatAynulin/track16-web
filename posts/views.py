import operator
from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from comments.forms import CommentForm
from comments.models import Comment
from posts.forms import SearchForm
from .models import Post


class PostList(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts_list'
    model = Post
    form_class_search = SearchForm

    def get_queryset(self):
        if self.q:
            return Post.objects.filter(Q(description__contains=self.q) | Q(title__contains=self.q)).order_by(self.order)
        for post in Post.objects.all():  # fix me
            post.count_score()
            post.save()
        return Post.objects.order_by(self.order)

    def dispatch(self, request, *args, **kwargs):
        self.order = kwargs.get('order')
        self.q = ""
        self.search_form = SearchForm(request.GET or None)
        if self.search_form.is_valid():
            self.q = self.search_form.cleaned_data['q']
        return super(PostList, self).dispatch(request, *args, **kwargs)


class PostDetail(CreateView):
    model = Comment
    template_name = 'posts/detail.html'
    fields = ('comment',)

    def dispatch(self, request, pk=None, *args, **kwargs):
        # when I used name 'post' instead of 'current_post', it rewrited field post (it's post request),
        # and some **it happened
        self.current_post = get_object_or_404(Post, id=pk)
        print(self.current_post)
        return super(PostDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.current_post
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.current_post
        return super(PostDetail, self).form_valid(form)

    def get_success_url(self):
        return '.'


class CreatePostView(CreateView):
    template_name = 'posts/submit.html'
    model = Post
    fields = (
        'title',
        'url',
        'description',
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('posts:detail', kwargs=({'pk': self.object.id}))


class EditPostView(UpdateView):
    template_name = 'posts/edit.html'
    model = Post
    fields = (
        'title',
        'url',
        'description'
    )

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('posts:detail', kwargs=({'pk': self.object.id}))
