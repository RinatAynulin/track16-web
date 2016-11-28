from django.conf.urls import url

from comments.views import EditCommentView, EditCommentFormView
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # ex: /comments/
    url(r'^$', views.index, name='index'),
    # ex: /comments/5/
    url(r'^(?P<pk>[0-9]+)/$', login_required(EditCommentView.as_view()), name='edit'),
    url(r'^edit_form/(?P<pk>[0-9]+)/$', login_required(EditCommentFormView.as_view()), name='edit_form'),
]
