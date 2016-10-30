from django.conf.urls import url

from comments.views import EditCommentView
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # ex: /comments/
    url(r'^$', views.index, name='index'),
    # ex: /comments/5/
    url(r'^(?P<pk>[0-9]+)/$', login_required(EditCommentView.as_view()), name='edit'),
]
