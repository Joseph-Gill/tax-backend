from django.contrib import admin

from app.social.models.comments import Comment
from app.social.models.posts import Post

admin.site.register(Post)
admin.site.register(Comment)
