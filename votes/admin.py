from django.contrib import admin
from .models import PostVote, CommentVote

admin.site.register(PostVote)
admin.site.register(CommentVote)    
