from rest_framework import (
    exceptions,
    serializers,
)

from .models import (
    Content,
    ContentGrant,
    ContentGrantUser,
    ContentGrantScope,
)


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            'uuid',
            'label',
            'text',
            'file',
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
        return instance


class ContentGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentGrant
        fields = [
            'name',
            'created_user',
            'created_time',
            'modified_time',
        ]
        read_only_fields = [
            'created_user',
            'created_time',
            'modified_time',
        ]


class ContentGrantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentGrantUser
        fields = [
            'user',
        ]


class ContentGrantScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentGrantScope
        fields = [
            'scope',
        ]
