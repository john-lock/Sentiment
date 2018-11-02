import unittest
import requests
from app import app


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testPage(self):
        """
        Test page is shortened version of a star trek script (source = http://chakoteya.net/NextGen/244.htm )
        """
        url = 'https://sentiment.johnlock.nl/testpage'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def testScore(self):
        with app.test_client() as client:
            sent = {'urlInput': 'https://sentiment.johnlock.nl/testpage'}
            result = client.post('/', data=sent)
            self.assertIn('<div class="progress-bar bg-success" style="width:23.0%">', str(result.data))
            self.assertIn('', str(result.data))

    def testQuotes(self):
        with app.test_client() as client:
            sent = {'urlInput': 'https://sentiment.johnlock.nl/testpage'}
            result = client.post('/', data=sent)
            self.assertIn("Most negative:</b> PICARD: No.\\n            <br>Score: -0.296", str(result.data))

    def testTable(self):
        with app.test_client() as client:
            sent = {'urlInput': 'https://sentiment.johnlock.nl/testpage'}
            result = client.post('/', data=sent)
            self.assertIn("<td>      Starship Mine Stardate: 46682.4 Original Airdate: 29 Mar, 1993", str(result.data))

    def testChart(self):
        with app.test_client() as client:
            sent = {'urlInput': 'https://sentiment.johnlock.nl/testpage'}
            result = client.post('/', data=sent)
            self.assertIn("0.0, 0.4019, 0.7269, 0.0, 0.4576, 0.0, 0.4019, 0.0, 0.0, 0.4019, -0.1531,", str(result.data))


if __name__ == '__main__':
    unittest.main()
