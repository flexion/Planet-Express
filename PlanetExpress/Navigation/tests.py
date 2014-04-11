import unittest
import json

from navigation import Navigator
from settings import settings


class NavigatorTest(unittest.TestCase, Navigator):

    def get_servers_v2(self):
        response = self.navigator.get_servers(version=2, region='DFW')
        if response['status_code'] != 200:
            self.fail(response['text'])

    def get_servers_v1(self):
        response = self.navigator.get_servers(version=1)
        if response['status_code'] != 200:
            self.fail(response['text'])

    def setUp(self):
        self.navigator = Navigator()
        response = self.navigator.log_in(username=settings.ACCOUNTS['rax-ord-ng']['USERNAME'],
                                         api_key=settings.ACCOUNTS['rax-ord-ng']['API_KEY'])
        if response['status_code'] != 200:
            self.fail(response['text'])

        #self.get_servers_v1()
        self.get_servers_v2()

    def tearDown(self):
        pass

    def test_has_ng_server_list(self):
        self.assertIsInstance(self.navigator.ng_servers, list)

    def test_has_fg_server_list(self):
        self.assertIsInstance(self.navigator.fg_servers, list)

if __name__ == '__main__':
    unittest.main()
