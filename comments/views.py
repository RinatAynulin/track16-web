from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView

from .models import Comment

def index(request):
    latest_comments_list = Comment.objects.order_by('created_at')
    template = loader.get_template('comments/index.html')
    context = {
        'latest_comments_list' : latest_comments_list,
    }
    return HttpResponse(template.render(context, request))

# def detail(request, comment_id):
#     try:
#         comment = Comment.objects.get(pk=comment_id)
#     except Comment.DoesNotExist:
#         raise Http404("Comment does not exist")
#     template = loader.get_template('comments/detail.html')
#     context = {
#         'comment' : comment,
#     }
#     return HttpResponse(template.render(context, request))

class EditCommentView(UpdateView):
    template_name = 'comments/detail.html'
    model = Comment
    fields = (
        'comment',
    )

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


    def get_success_url(self):
        return reverse('posts:detail', kwargs=({'pk': self.object.post.id}))

class EditCommentFormView(UpdateView):
    template_name = 'comments/edit.html'
    model = Comment
    fields = (
        'comment',
    )

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('posts:detail', kwargs=({'pk': self.object.post.id}))

    def form_valid(self, form):
        response = super(EditCommentFormView, self).form_valid(form)
        return HttpResponse('success')