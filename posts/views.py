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
        search_form = self.form_class_search(self.request.GET)
        order = self.order
        if search_form.is_valid():
            return Post.objects.filter(Q(description__contains=search_form.cleaned_data['q']) | Q(title__contains=search_form.cleaned_data['q'])).order_by(order)
        for post in Post.objects.all(): #fix me
            post.count_score()
            post.save()
        return Post.objects.order_by(order)

    def dispatch(self, request, *args, **kwargs):
        self.order = kwargs.get('order')
        self.search_form = SearchForm(request.GET or None)
        return super(PostList, self).dispatch(request, *args, **kwargs)  # error when empty fixme



class PostDetail(CreateView):
    model = Comment
    template_name = 'posts/detail.html'
    fields = ['comment']

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.post
        # context['form'] = self.form
        return context

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.post = get_object_or_404(Post, id=pk)
        self.object = self.get_object()
        # print(super(PostDetail, self))
        self.form = CommentForm(request.POST or None)
        if request.method == 'POST':
            if self.form.is_valid():
                comment = self.form.save(commit=False)
                comment.user = request.user
                comment.post = self.post
                comment.save()
                return redirect(self.get_success_url())
        return super(PostDetail, self).dispatch(request, *args, **kwargs)  # error when empty fixme

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     #form.instance.post = self.post
    #     return super(PostDetail, self).form_valid(form)


    def get_success_url(self):
        return reverse('posts:detail', kwargs=({'pk': self.post.id}))


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
