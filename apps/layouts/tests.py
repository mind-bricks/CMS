import os

from rest_framework import (
    reverse,
    status,
    test,
)

from ..mocks import AuthenticationMock


class LayoutTest(test.APITestCase):
    fixtures = [
        os.path.join('fixtures', 'test_grants.json'),
        os.path.join('fixtures', 'test_layouts.json'),
    ]

    def test_create_layout(self):
        url_list = reverse.reverse('layouts:layouts-list')
        response = self.client.post(url_list, data={'name': 'test-layout'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock('test-user') as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(
                url_list, data={'name': 'test-layout'})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with AuthenticationMock('test-user', user_scope=['cms.users']) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'name': 'test-layout-1',
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get('name'), 'test-layout-1')
            self.assertIn('read_grant', response.data)
            self.assertIn('write_grant', response.data)

            response = self.client.post(url_list, data={
                'name': 'test-layout-2',
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
                'name': 'test-layout-2',
                'read_grant': '10e7b066-4740-11ea-810e-a86bad54c153',
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get('name'), 'test-layout-2')
            self.assertEqual(
                str(response.data.get('read_grant')),
                '10e7b066-4740-11ea-810e-a86bad54c153',
            )

    def test_destroy_layout(self):
        url_detail = reverse.reverse('layouts:layouts-detail', [
            'cde619ee-4878-11ea-810e-a86bad54c153'
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

    def test_list_layout(self):
        url_list = reverse.reverse('layouts:layouts-list')
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
                url_list, QUERY_STRING='parent__isnull=false')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 0)

            # response = self.client.get(
            #     url_list,
            #     QUERY_STRING='uuid__in=cde619ee-4878-11ea-810e-a86bad54c153 '
            #                  'd9b6f770-4878-11ea-810e-a86bad54c153',
            # )
            # self.assertEqual(response.status_code, status.HTTP_200_OK)
            # self.assertEqual(response.data.get('count'), 2)

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

    def test_retrieve_layout(self):
        url_detail_1 = reverse.reverse('layouts:layouts-detail', [
            'cde619ee-4878-11ea-810e-a86bad54c153'
        ])
        url_detail_2 = reverse.reverse('layouts:layouts-detail', [
            'd9b6f770-4878-11ea-810e-a86bad54c153'
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

    def test_update_layout(self):
        url_detail_1 = reverse.reverse('layouts:layouts-detail', [
            'cde619ee-4878-11ea-810e-a86bad54c153'
        ])
        url_detail_2 = reverse.reverse('layouts:layouts-detail', [
            'd9b6f770-4878-11ea-810e-a86bad54c153'
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


class LayoutElementTest(test.APITestCase):
    fixtures = [
        os.path.join('fixtures', 'test_contents.json'),
        os.path.join('fixtures', 'test_layouts.json'),
        os.path.join('fixtures', 'test_grants.json'),
    ]

    def test_list_element(self):
        url_list = reverse.reverse(
            'layouts:layout-elements-list',
            ['cde619ee-4878-11ea-810e-a86bad54c153'],
        )
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)

        url_list = reverse.reverse(
            'layouts:layout-elements-list',
            ['d9b6f770-4878-11ea-810e-a86bad54c153'],
        )
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)

        with AuthenticationMock(
                'test-user',
                user_uuid='33878ba6-43d4-11ea-810e-a86bad54c153',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.get(url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), 1)

    def test_create_element(self):
        url_list = reverse.reverse(
            'layouts:layout-elements-list',
            ['cde619ee-4878-11ea-810e-a86bad54c153'],
        )
        response = self.client.post(url_list, data={
            'name': 'test-element',
            'content': '1370cd16-43c3-11ea-810e-a86bad54c153'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'name': 'test-element',
                'content': '1370cd16-43c3-11ea-810e-a86bad54c153'
            })
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.post(url_list, data={
                'name': 'test-element',
                'content': '1370cd16-43c3-11ea-810e-a86bad54c153'
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(
                str(response.data.get('content')),
                '1370cd16-43c3-11ea-810e-a86bad54c153',
            )

    def test_destroy_element(self):
        url_detail = reverse.reverse(
            'layouts:layout-elements-detail',
            [
                'd9b6f770-4878-11ea-810e-a86bad54c153',
                'test-layout-2-element-1',
            ],
        )
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with AuthenticationMock(
                'test-user',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        with AuthenticationMock(
                'test-user',
                user_uuid='3384bb3a-43c3-11ea-810e-a86bad54c153',
        ) as m:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {}'.format(m.access_token))
            response = self.client.delete(url_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_element(self):
        pass

    def test_retrieve_element(self):
        pass
