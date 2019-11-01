from django.contrib import admin
from .models import Post, ClapComment, Comment, ClapPost, CodeSnippet

admin.site.register(Post)
admin.site.register(ClapPost)
admin.site.register(Comment)
admin.site.register(ClapComment)
admin.site.register(CodeSnippet)