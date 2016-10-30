from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models import Sum

from votes.models import PostVote, CommentVote
from comments.models import Comment

class Post(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)

    def count_score(self):
        self.score = PostVote.objects.filter(post=self).aggregate(models.Sum('vote_type')).get('vote_type__sum') or 0

    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    def __unicode__(self):
        return 'Title: {}'.format(self.title)
