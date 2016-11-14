from __future__ import unicode_literals

from django.db import models
from django.conf import settings

VOTE_TYPES = (
    (1, 'UP'),
    (-1, 'DOWN'),
)

class PostVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey('posts.Post')
    vote_type = models.IntegerField(choices=VOTE_TYPES)

    #fixme

    def __unicode__(self):
        return 'User: {} \n Post: {} \n Vote: {}'.format(self.user.username, self.post.title, self.vote_type)


class CommentVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.ForeignKey('comments.Comment')
    vote_type = models.IntegerField(choices=VOTE_TYPES)

    def __unicode__(self):
        return 'User: {} \n Comment: {} \n Vote: {}'.format(self.user.username, self.post.title, self.vote_type)
