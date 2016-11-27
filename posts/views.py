import operator
from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from comments.forms import CommentForm
from comments.models import Comment
from posts.forms import SearchForm
from votes.models import PostVote
from .models import Post


class PostList(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts_list'
    model = Post
    form_class_search = SearchForm

    def get_queryset(self):
        if self.q:
            return Post.objects.filter(Q(description__contains=self.q) | Q(title__contains=self.q)).order_by(self.order)
        for post in Post.objects.all():  # fixme
            post.count_score()
            post.save()
        return Post.objects.order_by(self.order)

    def dispatch(self, request, *args, **kwargs):
        self.order = kwargs.get('order')
        self.q = ""
        self.search_placeholder = "search"
        self.search_form = SearchForm(request.GET or None)
        if self.search_form.is_valid():
            self.q = self.search_form.cleaned_data['q']
            self.search_placeholder = self.q
        return super(PostList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['search_placeholder'] = self.search_placeholder
        return context


class PostDetail(CreateView):
    model = Comment
    template_name = 'posts/detail.html'
    fields = ('comment',)

    def dispatch(self, request, pk=None, *args, **kwargs):
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
        return reverse('posts:detail', kwargs=({'pk': self.current_post.id}))


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


def opposite_type(vote_type):
    vote_type = int(vote_type)
    if vote_type is 1:
        return -1
    else:
        return 1


class PostLikesCountView(View):
    current_post = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=pk)
        return super(PostLikesCountView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        self.current_post.count_score()
        return HttpResponse(self.current_post.score)

    def post(self, request):
        user = request.user
        vote_type = request.POST.get("vote-type")
        likes_count = self.current_post.score
        if not PostVote.objects.filter(user=user, post=self.current_post,
                                       vote_type=vote_type).exists():

            if PostVote.objects.filter(user=user, post=self.current_post,
                                       vote_type=opposite_type(vote_type)).exists():
                vote = PostVote.objects.filter(user=user, post=self.current_post,
                                               vote_type=opposite_type(vote_type))[0]
                vote.vote_type = vote_type
                vote.save()
            else:
                vote = PostVote()
                vote.user = user
                vote.post = self.current_post
                vote.vote_type = vote_type
                vote.save()
            self.current_post.count_score()
            likes_count = self.current_post.score
        return HttpResponse(likes_count)


class PostLikes(View):
    def get(self, request):
        ids = request.GET.get('ids', '')
        ids = ids.split(',')
        for post in Post.objects.filter(id__in=ids):
            post.count_score()
            post.save()  # fixme wtf
        posts = dict(Post.objects.filter(id__in=ids).values_list('id', 'score'))
        return JsonResponse(posts)
