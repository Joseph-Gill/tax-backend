from django.conf import settings
from django.db import models

from app.social.models.posts import Post


class Comment(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clap_comment',
    )

    post = models.ForeignKey(
        verbose_name='post',
        to=Post,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    comment = models.CharField(
        verbose_name='comment',
        max_length=1000,
    )

    created = models.DateTimeField(
        verbose_name='created time',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user} post a comment: {self.comment[:20]}..."
