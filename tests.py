import unittest
import requests
import app


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app()

    def testpage(self):
        url = 'https://sentiment.johnlock.nl/test'
        response = requests.get(url)
        print(response.text)
        # self.assertEqual(,response.text)

    def test_score(self):
        data = {'urlInput': 'https://sentiment.johnlock.nl/test'}
        post_response = requests.post(url='https://sentiment.johnlock.nl', data=data)
        print(post_response)
        return post_response


if __name__ == '__main__':
    unittest.main()


# test can get scores
# test front end if possible