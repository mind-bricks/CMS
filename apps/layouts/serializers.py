from django.apps import apps
from rest_framework import (
    exceptions,
    serializers,
)

from .models import (
    Layout,
    LayoutElement,
)


class LayoutSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Layout.objects.all(),
        required=False,
        default=None,
    )
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
        model = Layout
        fields = [
            'uuid',
            'name',
            'parent',
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
        if instance.id == instance.parent:
            raise exceptions.ValidationError(
                'recursive reference'
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


class LayoutElementSerializer(serializers.ModelSerializer):
    content = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model('contents', 'Content').objects.all(),
    )

    class Meta:
        model = LayoutElement
        fields = [
            'name',
            'content',
            'created_time',
            'modified_time',
        ]
        read_only_fields = [
            'created_time',
            'modified_time',
        ]
