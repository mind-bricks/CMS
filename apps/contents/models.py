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
        'ContentGrant',
        null=True,
        default=None,
        related_name='read_content',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    write_grant = models.ForeignKey(
        'ContentGrant',
        null=True,
        default=None,
        related_name='write_content',
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


class ContentGrant(models.Model):
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


class ContentGrantUser(models.Model):
    grant = models.ForeignKey(
        ContentGrant,
        related_name='users',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    user = models.UUIDField()

    class Meta:
        unique_together = [
            ('grant', 'user')
        ]


class ContentGrantScope(models.Model):
    grant = models.ForeignKey(
        ContentGrant,
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
