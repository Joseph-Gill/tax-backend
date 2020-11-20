from django.db import models


class Task(models.Model):
    # This likely needs to be Many_to_One or Many_to_Many field tied to User_Profile, need more info from Alain
    responsible_user = models.CharField(
        max_length=150
    )

    planned_completion_date = models.DateField()

    due_date = models.DateField()

    description = models.TextField()

    documents = models.FileField(
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateField(
        auto_now=True
    )

    def __str__(self):
        return f'Task #{self.pk}'
