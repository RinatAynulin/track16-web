from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /comments/
    url(r'^$', views.index, name='index'),
    # ex: /comments/5/
    url(r'^(?P<comment_id>[0-9]+)/$', views.detail, name='detail'),
]
