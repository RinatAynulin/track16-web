from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', related_name='post_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set')

    def __unicode__(self):
        return 'By {}: \n {} \n at {}'.format(self.user, self.comment, self.created_at)
