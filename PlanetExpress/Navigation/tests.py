import unittest


class LoginTest(unittest.TestCase, Navigator):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def loginTest(self):
        Naviator.log_in()

if __name__ == '__main__':
    LoginTest(Navigator())
