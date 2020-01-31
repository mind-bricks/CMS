from django.utils.translation import ugettext_lazy as _
from rest_framework import (
    authentication,
    exceptions,
)

from .authentication import UMSOAuth2


class AnonymousUser(object):
    id = None
    pk = id
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False

    def __init__(self):
        pass

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def get_username(self):
        return self.username

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False


class AuthenticatedUser(object):
    is_staff = False
    is_active = True
    is_superuser = False

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return 'AuthenticatedUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.pk

    def get_username(self):
        return self.user.get('username')

    @property
    def id(self):
        return self.user.get('uuid')

    @property
    def pk(self):
        return self.user.get('uuid')

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def scopes(self):
        return self.user.get('scopes', [])

    @property
    def uuid(self):
        return self.user.get('uuid')

    @property
    def username(self):
        return self.user.get('username')


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
