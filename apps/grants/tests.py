import os

from rest_framework import (
    reverse,
    status,
    test,
)

from ..mocks import AuthenticationMock


class GrantTest(test.APITestCase):
    fixtures = [os.path.join('fixtures', 'test_grants.json')]

    def test_create_grant(self):
        url_list = reverse.reverse('grants:grants-list')
        response = self.client.post(url_list, data={'name': 'test-grant'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={'name': 'test-grant'})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={'name': 'test-grant'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant(self):
        url_detail = reverse.reverse('grants:grants-detail', [
            '32e5cf68-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_grant(self):
        url_list = reverse.reverse('grants:grants-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 2)

            response = self.client.get(
                url_list, QUERY_STRING='name=default-read')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_retrieve_grant(self):
        url_detail = reverse.reverse('grants:grants-detail', [
            '32e5cf68-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_detail)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_grant(self):
        url_detail = reverse.reverse('grants:grants-detail', [
            '32e5cf68-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.patch(url_detail, data={'name': 'tmp'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail, data={'name': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('name'), 'tmp')

    def test_list_grant_user(self):
        url_list = reverse.reverse('grants:grant-users-list', [
            '10e7b066-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_create_grant_user(self):
        url_list = reverse.reverse('grants:grant-users-list', [
            '10e7b066-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.post(url_list, data={
            'user': '51efaebc-4405-11ea-810e-a86bad54c153'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'user': '51efaebc-4405-11ea-810e-a86bad54c153'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant_user(self):
        url_detail = reverse.reverse('grants:grant-users-detail', [
            '10e7b066-4740-11ea-810e-a86bad54c153',
            '1fad22e4-43d4-11ea-810e-a86bad54c153',
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_grant_scope(self):
        url_list = reverse.reverse('grants:grant-scopes-list', [
            '10e7b066-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_create_grant_scope(self):
        url_list = reverse.reverse('grants:grant-scopes-list', [
            '10e7b066-4740-11ea-810e-a86bad54c153'
        ])
        response = self.client.post(url_list, data={'scope': 'scope.tmp'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={'scope': 'scope.tmp'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant_scope(self):
        url_detail = reverse.reverse('grants:grant-scopes-detail', [
            '32e5cf68-4740-11ea-810e-a86bad54c153',
            'users.admin',
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
