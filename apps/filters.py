from uuid import UUID

from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import filters


class UUIDListField(forms.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid list of UUID.'),
    }

    def prepare_value(self, value):
        if isinstance(value, list):
            return ' '.join(
                v.hex for
                v in value if isinstance(v, UUID)
            )
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None

        if not isinstance(value, list):
            try:
                value = [
                    UUID(v.strip()) for
                    v in value.split(' ') if
                    v.strip()
                ]
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid'
                )
        return value


class UUIDListFilter(filters.Filter):
    field_class = UUIDListField
