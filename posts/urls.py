from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /post/
    url(r'^$', views.index, name='index'),
    # ex: /posts/5/
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
]
