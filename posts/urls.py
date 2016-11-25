from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # ex: /post/
    url(r'^$', views.PostList.as_view(), {'order':'-created_at'}, name='index'),
    url(r'^hot/', views.PostList.as_view(ordering='-score'), {'order':'-score'}, name='index_hot'),
    # ex: /posts/5/
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/likes$', views.PostLikesCountView.as_view(), name='likes'),
    url(r'^likes$', views.PostLikes.as_view(), name='likes'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditPostView.as_view(), name='edit'),
    url(r'^submit/$', login_required(views.CreatePostView.as_view()), name='submit'),
]
