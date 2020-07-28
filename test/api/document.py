import unittest

from requests import get, post, put, delete

api_version = 1
host = '127.0.0.1'
port = 5000
base_url = f'http://{host}:{port}/api/v{api_version}'


class ApiTestCase(unittest.TestCase):
    def test_api_project_get(self):
        response = get(f'{base_url}/projects')
        status = response.json()['status']
        self.assertEqual('success', status)

    def test_api_project_post(self):
        data = {'name': 'Mark 1', 'description': 'Parker'}
        response = post(f'{base_url}/projects', data=data)
        status = response.json()['status']
        self.assertEqual('success', status)

    def test_api_project_post_fail(self):
        data = {'name': 'Mark 1'}
        response = post(f'{base_url}/projects', data=data)
        status = response.json()['status']
        self.assertIn('fail', status)

    def test_api_project_update(self):
        data = {'name': 'Mark 1', 'description': 'Parker'}
        response = post(f'{base_url}/projects', data=data)
        project_id = response.json()['data']['id']
        data = {'name': 'Mark 3'}
        response = put(f'{base_url}/projects/{project_id}', data=data)
        status = response.json()['status']
        self.assertEqual('success', status)

    def test_api_project_update_fail(self):
        data = {'name': 'Mark 1', 'description': 'Parker'}
        response = post(f'{base_url}/projects', data=data)
        project_id = response.json()['data']['id']
        data = {'name': 'Mark 3', 'unknown': 0}
        response = put(f'{base_url}/projects/{project_id}', data=data)
        status = response.json()['status']
        self.assertEqual('fail', status)

    def test_api_project_delete_all(self):
        response = get(f'{base_url}/projects')
        for project in response.json()['data']:
            project_id = project['id']
            response = delete(f'{base_url}/projects/{project_id}')
            self.assertNotIn('errors', response.json())
        response = get(f'{base_url}/projects')
        data = response.json()['data']
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
