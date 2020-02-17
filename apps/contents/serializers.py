from django.apps import apps
from rest_framework import (
    exceptions,
    serializers,
)

from .models import (
    Content,
)


class ContentSerializer(serializers.ModelSerializer):
    read_grant = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model('grants', 'Grant').objects.all(),
        required=False,
    )
    write_grant = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model('grants', 'Grant').objects.all(),
        required=False,
    )

    class Meta:
        model = Content
        fields = [
            'uuid',
            'label',
            'text',
            'file',
            'is_public',
            'read_grant',
            'write_grant',
            'created_user',
            'created_time',
            'modified_time',
        ]
        read_only_fields = [
            'uuid',
            'created_user',
            'created_time',
            'modified_time',
        ]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        if (
                not instance.text and
                not instance.file
        ):
            raise exceptions.ValidationError(
                'either text or file should be specified'
            )

        if ((
                instance.read_grant and
                str(instance.created_user) !=
                str(instance.read_grant.created_user)
        ) or (
                instance.write_grant and
                str(instance.created_user) !=
                str(instance.write_grant.created_user)
        )):
            raise exceptions.ValidationError(
                'grants mismatch'
            )

        return instance
