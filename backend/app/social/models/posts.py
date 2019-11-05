from django.db import models


class Post(models.Model):
    social_profile = models.ForeignKey(
        verbose_name='social user profile',
        to='SocialProfile',
        on_delete=models.CASCADE,
        related_name='posts',
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
        return f"{self.social_profile}: {self.content[:50]} ..."
