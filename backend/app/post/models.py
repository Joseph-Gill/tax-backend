from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
    )
    content = models.TextField(
        verbose_name='content'
    )
    created = models.DateTimeField(
        verbose_name='created',
        auto_now_add=True,
    )

    shared = models.ForeignKey(
        verbose_name='shared post',
        to='self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sharing_posts'
    )

    def __str__(self):
        return f"{self.user}: {self.content[:50]} ..."


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
