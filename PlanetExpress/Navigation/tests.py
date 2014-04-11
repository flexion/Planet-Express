import unittest

from navigation import Navigator
from settings import settings

class LoginTest(unittest.TestCase, Navigator):

    def setUp(self):
        self.navigator = Navigator()

    def tearDown(self):
        pass

    def test_can_log_in(self):
        response = self.navigator.log_in(username=settings.ACCOUNTS['rax-ord-ng']['USERNAME'],
                                         api_key=settings.ACCOUNTS['rax-ord-ng']['API_KEY'])
        if response['status_code'] != 200:
            self.fail(response['text'])


if __name__ == '__main__':
    unittest.main()
