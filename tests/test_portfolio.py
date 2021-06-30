import json

from . import BaseTestClass


class PortfolioClientTestCase(BaseTestClass):

    def test_get_all(self):
        res = self.client.get('/portfolio/')

        actual = len(json.loads(res.data))

        expected = 30

        self.assertEqual(200, res.status_code)
        self.assertEqual(expected, actual)

    def test_get(self):
        res = self.client.get('/portfolio/1')

        actual = json.loads(res.data)

        expected = {'idportfolio': 1,
                    'description': 'Tyrion of House Lannister. Imp, Halfman. Never forget what you are, for surely the world will not. Not affiliated with #GameofThrones or HBO ++++--2',
                    'image_url': 'https://pbs.twimg.com/profile_images/668279339838935040/8sUE9d4C_400x400.jpg',
                    'twitter_user_name': 'GoT_Tyrion',
                    'title': 'Tyrion Lannister',
                    'user_id': '',
                    'experience_summary': None,
                    'last_names': None,
                    'names': None,
                    'twitter_user_id': None}

        self.assertEqual(200, res.status_code)
        self.assertEqual(expected, actual)

    def test_get_not_found(self):
        res = self.client.get('/portfolio/9999')
        self.assertEqual(404, res.status_code)

    def test_put_no_payload(self):
        res = self.client.put('/portfolio/2', headers={'content-type': 'application/json'})
        self.assertEqual(400, res.status_code)

    def test_put(self):
        with self.app.test_client() as client:
            res = client.get('/portfolio/2')

            actual = json.loads(res.data)
            actual['twitter_user_name'] = actual['twitter_user_name'].upper()

            expected = {'idportfolio': 2,
                        'description': 'Daenerys is one of the last surviving members (along with her older brother, Viserys) of House Targaryen which, until 14 years before the events of the first novel',
                        'image_url': 'https://pbs.twimg.com/profile_images/1117967801652617216/i8PWXebo_400x400.jpg',
                        'twitter_user_name': 'DAENERYS',
                        'title': 'Daenerys Targaryen',
                        'user_id': '',
                        'experience_summary': None,
                        'last_names': None,
                        'names': None,
                        'twitter_user_id': None}

            res = client.put('/portfolio/2', data=json.dumps(expected), headers={'content-type': 'application/json'})

            self.assertEqual(302, res.status_code)
            self.assertEqual(res.request.path, '/portfolio/2')

    def test_get_tweets(self):
        res = self.client.get('/portfolio/1/tweets')

        actual = len(json.loads(res.data))

        expected = 5

        self.assertEqual(200, res.status_code)
        self.assertEqual(expected, actual)

    def test_get_tweets_not_found(self):
        res = self.client.get('/portfolio/99999/tweets')
        self.assertEqual(404, res.status_code)

    def test_get_tweets_not_tweets(self):
        res = self.client.get('/portfolio/3/tweets')

        actual = len(json.loads(res.data))

        self.assertEqual(200, res.status_code)
        self.assertEqual(0, actual)
