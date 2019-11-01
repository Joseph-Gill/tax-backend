from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

JAVASCRIPT = 'JS'
PYTHON = 'PY'
HTML = 'HT'
CSS = 'CS'
Langs = [
    (JAVASCRIPT, 'JAVASCRIPT'),
    (PYTHON, 'PYTHON'),
    (HTML, 'HTML'),
    (CSS, 'CSS'),
]


class CodeSnippet(models.Model):
    code = models.TextField(
        verbose_name="code snippet",
        blank=True,
        null=True,
    )
    prog_language = models.CharField(
        max_length=2,
        choices=Langs,
        default=JAVASCRIPT,
        null=True,
        blank=True,
    )


class Website(models.Model):
    url = models.TextField(
        verbose_name="link to share",
        blank=True,
        null=True,
    )
    saved_website = models.TextField(
        blank=True,
        null=True
    )
    title = models.TextField(
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    image_url = models.URLField(
        blank=True,
        null=True
    )


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
    code_snippet = models.OneToOneField(
        verbose_name="code snippet",
        to=CodeSnippet,
        on_delete=models.SET_NULL,
        related_name='post',
        blank=True,
        null=True,
    )
    website = models.OneToOneField(
        verbose_name='saved website',
        to=Website,
        on_delete=models.SET_NULL,
        related_name='post',
        null=True,
        blank=True

    )

    category = models.CharField(

        verbose_name="category",
        max_length=20,
        default='FullStack',
        choices=(
            ('FS', 'Full Stack'),
            ('FE', 'Frontend'),
            ('BE', 'Backend'),
            ('DS', 'Data Science'),
        )
    )
    check_to_save = models.BooleanField(
        verbose_name="Should the website be saved?",
        default=False
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


class ClapComment(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='user',
        null=True,
    )

    comment = models.ForeignKey(
        verbose_name='comment',
        to=Comment,
        related_name='claps',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} | {self.comment}"


class ClapPost(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='claps',
        null=True,
    )
    post = models.ForeignKey(
        verbose_name='post',
        to=Post,
        related_name='claps',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} | {self.post}"
