import unittest
import requests
import app


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app()

    def testpage(self):
        url = 'https://sentiment.johnlock.nl/testpage'
        response = requests.get(url)
        print(response.text)
        # self.assertEqual(,response.text)

    def test_score(self):
        url = 'https://sentiment.johnlock.nl/test'
        response = requests.get(url)
        print(response)
        return response


if __name__ == '__main__':
    unittest.main()


# test can get scores
# test front end if possible