import os

from rest_framework import (
    reverse,
    status,
    test,
)

from ..mocks import AuthenticationMock


class ContentTest(test.APITestCase):
    fixtures = [
        os.path.join('fixtures', 'test_grants.json'),
        os.path.join('fixtures', 'test_contents.json'),
    ]

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

        with AuthenticationMock('test-user', user_scope=['cms.users']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'text': 'test-content-1',
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get('text'), 'test-content-1')
            self.assertIn('read_grant', response.data)
            self.assertIn('write_grant', response.data)
            self.assertIn('label', response.data)

            with open('README.md') as f:
                response = self.client.post(url_list, data={
                    'file': f,
                })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('file', response.data)

            response = self.client.post(url_list, data={
                'text': 'test-content-2',
                'read_grant': '10e7b066-4740-11ea-810e-a86bad54c153',
            })
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'text': 'test-content-2',
                'read_grant': '10e7b066-4740-11ea-810e-a86bad54c153',
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get('text'), 'test-content-2')
            self.assertEqual(
                str(response.data.get('read_grant')),
                '10e7b066-4740-11ea-810e-a86bad54c153',
            )

    def test_destroy_content(self):
        url_detail = reverse.reverse('contents:contents-detail', [
            '1370cd16-43c3-11ea-810e-a86bad54c153'
        ])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock('test-user', user_scope=['cms.users']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
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
                user_scope=['cms.users'],
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

            response = self.client.get(
                url_list,
                QUERY_STRING='uuid=1370cd16-43c3-11ea-810e-a86bad54c153',
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

            response = self.client.get(
                url_list,
                QUERY_STRING='uuid__in=1370cd16-43c3-11ea-810e-a86bad54c153 '
                             '5c12a9be-43c7-11ea-810e-a86bad54c153',
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 2)

        with AuthenticationMock(
                'test-user',
                user_uuid='1fad22e4-43d4-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
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
                user_scope=['cms.users'],
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

        with AuthenticationMock('test-user', user_scope=['cms.users']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_1, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_1, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        with AuthenticationMock(
                'test-user',
                user_uuid='33878ba6-43d4-11ea-810e-a86bad54c153',
                user_scope=['cms.users'],
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.patch(url_detail_2, data={'text': 'tmp'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
