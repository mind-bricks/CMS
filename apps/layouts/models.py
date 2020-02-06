from uuid import uuid1

from django.db import models


class Layout(models.Model):
    uuid = models.UUIDField(
        default=uuid1,
        unique=True,
    )
    name = models.CharField(
        max_length=64,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        default=None,
        related_name='children',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    is_public = models.BooleanField(
        default=False,
    )
    read_grant = models.ForeignKey(
        'grants.Grant',
        null=True,
        default=None,
        related_name='read_layouts',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    write_grant = models.ForeignKey(
        'grants.Grant',
        null=True,
        default=None,
        related_name='write_layouts',
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

    class Meta:
        unique_together = [
            ('parent', 'name'),
        ]


class LayoutElement(models.Model):
    layout = models.ForeignKey(
        Layout,
        related_name='elements',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    content = models.ForeignKey(
        'contents.Content',
        related_name='layouts',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
    )
    modified_time = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = [
            ('layout', 'name'),
        ]
