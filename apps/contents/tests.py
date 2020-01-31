import os

from rest_framework import (
    reverse,
    status,
    test,
)

from ..mocks import AuthenticationMock


class ContentTest(test.APITestCase):
    fixtures = [os.path.join('fixtures', 'test_contents.json')]

    def test_create_content(self):
        url_list = reverse.reverse('contents:contents-list')
        response = self.client.post(url_list, data={'text': 'test-content'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock('test-user') as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(
                url_list, data={'text': 'test-content'})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with AuthenticationMock('test-user', user_scope=['cms']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(
                url_list, data={'text': 'test-content'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get('text'), 'test-content')
            self.assertIn('label', response.data)

    def test_destroy_content(self):
        url_detail = reverse.reverse('contents:contents-detail', [
            '1370cd16-43c3-11ea-810e-a86bad54c153'
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock('test-user', user_scope=['cms']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_content(self):
        url_list = reverse.reverse('contents:contents-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 3)

            response = self.client.get(
                url_list, QUERY_STRING='label__contains=1')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

        with AuthenticationMock(
                'test-user',
                user_uuid='1fad22e4-43d4-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 2)

    def test_retrieve_content(self):
        url_detail_1 = reverse.reverse('contents:contents-detail', [
            '1370cd16-43c3-11ea-810e-a86bad54c153'
        ])
        url_detail_2 = reverse.reverse('contents:contents-detail', [
            '5c12a9be-43c7-11ea-810e-a86bad54c153'
        ])
        response = self.client.get(url_detail_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url_detail_2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_detail_1)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.get(url_detail_2)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_content(self):
        url_detail_1 = reverse.reverse('contents:contents-detail', [
            '1370cd16-43c3-11ea-810e-a86bad54c153'
        ])
        url_detail_2 = reverse.reverse('contents:contents-detail', [
            '5c12a9be-43c7-11ea-810e-a86bad54c153'
        ])
        response = self.client.patch(url_detail_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock('test-user', user_scope=['cms']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_1, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_1, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        with AuthenticationMock(
                'test-user',
                user_uuid='33878ba6-43d4-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_2, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContentGrantTest(test.APITestCase):
    fixtures = [os.path.join('fixtures', 'test_contents.json')]

    def test_create_grant(self):
        url_list = reverse.reverse('contents:content-grants-list')
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
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={'name': 'test-grant'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant(self):
        url_detail = reverse.reverse('contents:content-grants-detail', [
            'default-write'
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_grant(self):
        url_list = reverse.reverse('contents:content-grants-list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 2)

    def test_retrieve_grant(self):
        url_detail = reverse.reverse('contents:content-grants-detail', [
            'default-write'
        ])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_detail)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_grant(self):
        url_detail = reverse.reverse('contents:content-grants-detail', [
            'default-write'
        ])
        response = self.client.patch(url_detail, data={'name': 'tmp'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail, data={'name': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('name'), 'tmp')

    def test_list_grant_user(self):
        url_list = reverse.reverse('contents:content-grant-users-list', [
            'default-read'
        ])
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_create_grant_user(self):
        url_list = reverse.reverse('contents:content-grant-users-list', [
            'default-read'
        ])
        response = self.client.post(url_list, data={
            'user': '51efaebc-4405-11ea-810e-a86bad54c153'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'user': '51efaebc-4405-11ea-810e-a86bad54c153'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant_user(self):
        url_detail = reverse.reverse('contents:content-grant-users-detail', [
            'default-read',
            '1fad22e4-43d4-11ea-810e-a86bad54c153',
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_grant_scope(self):
        url_list = reverse.reverse('contents:content-grant-scopes-list', [
            'default-read'
        ])
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_create_grant_scope(self):
        url_list = reverse.reverse('contents:content-grant-scopes-list', [
            'default-read'
        ])
        response = self.client.post(url_list, data={'scope': 'scope.tmp'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={'scope': 'scope.tmp'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_grant_scope(self):
        url_detail = reverse.reverse('contents:content-grant-scopes-detail', [
            'default-write',
            'users.admin',
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
