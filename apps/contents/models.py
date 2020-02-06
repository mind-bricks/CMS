from uuid import uuid1

from django.db import models


class Content(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    label = models.CharField(
        max_length=32,
        blank=True,
        default='',
    )
    text = models.TextField(
        blank=True,
        null=True,
        default=None,
    )
    file = models.FileField(
        blank=True,
        null=True,
        default=None,
        upload_to='%Y-%m-%d',
    )
    is_public = models.BooleanField(
        default=False,
    )
    read_grant = models.ForeignKey(
        'grants.Grant',
        null=True,
        default=None,
        related_name='read_contents',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    write_grant = models.ForeignKey(
        'grants.Grant',
        null=True,
        default=None,
        related_name='write_contents',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    created_user = models.UUIDField()
    created_time = models.DateTimeField(
        auto_now_add=True,
    )
    modified_time = models.DateTimeField(
        auto_now=True,
    )
