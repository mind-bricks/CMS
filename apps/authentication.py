import datetime
import urllib.parse

import bson
import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework import status

UMS_OAUTH2_SETTINGS = getattr(settings, 'UMS_OAUTH2', {})


class UMSOAuth2(object):
    oauth2_cache_prefix = UMS_OAUTH2_SETTINGS.get(
        'CACHE_PREFIX', 'oauth2')
    oauth2_client_id = UMS_OAUTH2_SETTINGS.get(
        'CLIENT_ID', '')
    oauth2_client_secret = UMS_OAUTH2_SETTINGS.get(
        'CLIENT_SECRET', '')
    oauth2_url_scheme = UMS_OAUTH2_SETTINGS.get(
        'URL_SCHEME', 'http')
    oauth2_url_domain = UMS_OAUTH2_SETTINGS.get(
        'URL_DOMAIN', 'localhost')
    oauth2_login_path = UMS_OAUTH2_SETTINGS.get(
        'LOGIN_PATH', 'oauth2/token/')
    oauth2_introspect_path = UMS_OAUTH2_SETTINGS.get(
        'INTROSPECT_PATH', 'oauth2/introspect/')
    oauth2_login_url = '{}://{}/{}'.format(
        oauth2_url_scheme, oauth2_url_domain, oauth2_login_path)
    oauth2_introspect_url = '{}://{}/{}'.format(
        oauth2_url_scheme, oauth2_url_domain, oauth2_introspect_path)

    def make_introspect_cache_key(self):
        return '{}:{}'.format(
            self.oauth2_cache_prefix,
            self.oauth2_client_id,
        )

    def make_access_cache_key(
            self,
            access_token,
    ):
        return '{}:{}'.format(
            self.oauth2_cache_prefix,
            access_token,
        )

    def save_user_to_cache(
            self,
            access_token,
            user,
            expire,
            mutex=None,
    ):
        if not expire:  # cache user if need be
            return

        delta = (
            datetime.datetime.fromtimestamp(
                int(expire), datetime.timezone.utc) -
            datetime.datetime.now(datetime.timezone.utc)
        )
        expires_in = int(delta.total_seconds())
        if expires_in < 60:
            return

        expires_in -= 30
        expires_in = min(300, expires_in)
        cache.set(
            self.make_access_cache_key(access_token),
            bson.dumps(user),
            expires_in,
        )

        user_uuid = user.get('uuid')
        if not mutex or not user_uuid:
            return

        access_mutex_cache_key = '{}:{}:{}'.format(
            self.oauth2_cache_prefix, mutex, user_uuid)
        access_token_prev = cache.get(access_mutex_cache_key)
        cache.set(access_mutex_cache_key, access_token)
        if access_token_prev:
            cache.delete(self.make_access_cache_key(access_token_prev))

    def load_user_from_cache(self, access_token):
        data = cache.get(self.make_access_cache_key(access_token))
        return data and bson.loads(data) or {}

    def do_get_introspect_token(self):
        response = requests.post(self.oauth2_login_url, data={
            'grant_type': 'client_credentials',
            'client_id': self.oauth2_client_id,
            'client_secret': self.oauth2_client_secret,
        })
        if response.status_code != status.HTTP_200_OK:
            return None

        response = response.json()
        if response.get('error'):
            return None

        access_token = response.get('access_token')
        expires_in = int(response.get('expires_in'))
        expires_in = expires_in - 30
        if expires_in > 0:
            cache.set(
                self.make_introspect_cache_key(),
                access_token,
                expires_in,
            )

        return access_token

    def get_introspect_token(self):
        return (
            cache.get(self.make_introspect_cache_key()) or
            self.do_get_introspect_token()
        )

    def do_get_user_by_access_token(self, access_token):
        response = requests.post(
            self.oauth2_introspect_url,
            data={'token': access_token},
            headers={
                'Authorization': 'Bearer {}'.format(
                    self.get_introspect_token())
            }
        )
        if not response.ok:
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                # try refreshing introspect token
                self.do_get_introspect_token()
            return None

        response = response.json()
        scopes = response.get('scope')
        user = response.get('user') or {}
        if response.get('error'):
            return None

        scopes = scopes and scopes.split(' ') or []
        scopes = list(filter(None, scopes))
        user.update(scopes=scopes)

        self.save_user_to_cache(
            access_token, user,
            response.get('exp'),
            mutex=response.get('mutex')
        )
        return user

    def get_user_by_access_token(self, access_token):
        return (
            self.load_user_from_cache(access_token) or
            self.do_get_user_by_access_token(access_token)
        )

    def authorized_request(
            self,
            path,
            method='post',
            params=None,
            data=None,
            access_token=None,
            **kwargs
    ):
        bits = urllib.parse.urlsplit(path)
        location = (
            '{}://{}/{}'.format(
                self.oauth2_url_scheme, self.oauth2_url_domain, path)
            if not (bits.scheme and bits.netloc) else path
        )
        handler = getattr(requests, method.lower())
        response = handler(
            location,
            params=params,
            data=data,
            headers={
                'Authorization': 'Bearer {}'.format(
                    access_token or self.get_introspect_token())
            },
            **kwargs
        )

        try:
            response_json = response.json()
        except ValueError:
            response_json = {}

        return response.status_code, response_json
