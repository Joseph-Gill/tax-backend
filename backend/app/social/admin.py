from django.contrib import admin

from app.social.models.comments import Comment
from app.social.models.posts import Post
from app.social.models.profile import SocialProfile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SocialProfile)
