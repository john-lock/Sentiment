import unittest
import requests
import app

#app.create_app()

class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app()

    def test_testpage_score(self):
        url = 'http://jl-.herokuapp.com/test.html'
        response = requests.get(url)
        print(response.text)
        # self.assertEqaul(,response.text)

    #def test_testpage_  (self)

if __name__ == '__main__':
    unittest.main()


## fill test page with a copy of something
# test can get scores
# test front end if possible