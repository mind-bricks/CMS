from rest_framework import serializers

from .models import (
    Grant,
    GrantScope,
    GrantUser,
)


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = [
            'uuid',
            'name',
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


class GrantScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrantScope
        fields = [
            'scope',
        ]


class GrantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrantUser
        fields = [
            'user',
        ]
