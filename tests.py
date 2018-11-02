import unittest
import requests
from app import app


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testpage(self):
        url = 'https://sentiment.johnlock.nl/testpage'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def testscore(self):
        with app.test_client() as client:
            sent = {'urlInput': 'https://sentiment.johnlock.nl/testpage'}
            result = client.post('/', data=sent)
            print(result.data)
            self.assertIn("Most negative: NEIL: No.", str(result.data))


if __name__ == '__main__':
    unittest.main()


# test can get scores
# test front end if possible
