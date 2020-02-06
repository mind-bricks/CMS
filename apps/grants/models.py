from uuid import uuid1

from django.db import models


class Grant(models.Model):
    uuid = models.UUIDField(
        default=uuid1,
        unique=True,
    )
    name = models.TextField(
        blank=True,
        default='',
    )
    created_user = models.UUIDField()
    created_time = models.DateTimeField(
        auto_now_add=True,
    )
    modified_time = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = [
            ('name', 'created_user')
        ]


class GrantUser(models.Model):
    grant = models.ForeignKey(
        Grant,
        related_name='users',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    user = models.UUIDField()

    class Meta:
        unique_together = [
            ('grant', 'user')
        ]


class GrantScope(models.Model):
    grant = models.ForeignKey(
        Grant,
        related_name='scopes',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    scope = models.CharField(
        max_length=32,
    )

    class Meta:
        unique_together = [
            ('grant', 'scope')
        ]
