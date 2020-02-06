__all__ = [
    'AnonymousUser',
    'AuthenticatedUser',
    'SettingsAuthentication',
]

from django.utils.translation import ugettext_lazy as _
from rest_framework import (
    authentication,
    exceptions,
)

from .authentication import (
    AnonymousUser,
    AuthenticatedUser,
    UMSOAuth2,
)


class SettingsAuthentication(UMSOAuth2, authentication.BaseAuthentication):

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None

        if len(auth) == 1:
            msg = _(
                'Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                'Invalid token header. '
                'Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. '
                'Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        credentials = self.authenticate_credentials(token)
        if not credentials:
            msg = _(
                'Invalid token header. No user found.')
            raise exceptions.AuthenticationFailed(msg)

        return (
            credentials[0],
            credentials[1],
        )

    def authenticate_credentials(self, key):
        user = self.get_user_by_access_token(key)
        return user and (AuthenticatedUser(user), key) or None

    def authenticate_header(self, request):
        return 'Bearer'
