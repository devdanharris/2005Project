import unittest
from GroupProject import *


class TestGroups(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
        db.create_all()
        self.testApp = app.test_client()
        self.register("Daniel", "Harris")
        self.register("First", "pass")
        self.register("Second", "pass")
        self.register("Third", "pass")
        self.create_group("Test")
        self.create_group("Other")
        self.create_group("          ")
        self.create_group("54321")
        self.create_group("!!@@##")

    def tearDown(self):
        db.drop_all()

    def register(self, username, password):
        return self.testApp.post('/register', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.testApp.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.testApp.get('/logout', follow_redirects=True)

    def create_group(self, group_name):
        return self.testApp.post('/create_group', data=dict(
            group_name=group_name
        ), follow_redirects=True)

    def join_group(self, group_name):
        url = str("/join_group/" + str(group_name))
        return self.testApp.get(url, follow_redirects=True)

    def test_create_group_logged_in(self):
        self.login("Daniel", "Harris")
        test = self.create_group("Group One")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_create_group_logged_out(self):
        test = self.create_group("Group Two")
        assert b'Error: Must be logged in to create a group' in test.data

    @unittest.expectedFailure
    def test_create_group_duplicate(self):
        self.login("Daniel", "Harris")
        self.create_group("Group Three")
        test = self.create_group("Group Three")
        assert b'Group Successfully Created' in test.data
        self.logout()

    @unittest.expectedFailure
    def test_create_group_null_name(self):
        self.login("Daniel", "Harris")
        test = self.create_group("")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_create_group_symbols(self):
        self.login("Daniel", "Harris")
        test = self.create_group("~!@#$%^")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_create_group_whitespace(self):
        self.login("Daniel", "Harris")
        test = self.create_group("     ")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_create_group_integers(self):
        self.login("Daniel", "Harris")
        test = self.create_group("012345")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_create_group_over_char_limit(self):
        self.login("Daniel", "Harris")
        test = self.create_group("ithinkthattherearewaytoomanycharactersinthislineforagroupname")
        assert b'Group Successfully Created' in test.data
        self.logout()

    def test_join_group_logged_in(self):
        self.login("Daniel", "Harris")
        test = self.join_group("Test")
        assert b'joined the group' in test.data
        self.logout()

    @unittest.expectedFailure
    def test_join_group_logged_out(self):
        test = self.join_group("Test")
        assert b'joined the group' in test.data

    @unittest.expectedFailure
    def test_join_group_duplicate(self):
        self.login("First", "pass")
        self.join_group("Test")
        test = self.join_group("Test")
        assert b'joined the group' in test.data
        self.logout()

    def test_join_group_multiple(self):
        self.login("Second", "pass")
        self.join_group("Other")
        test = self.join_group("Test")
        assert b'joined the group' in test.data
        self.logout()

    def test_join_group_whitespace(self):
        self.login("Daniel", "Harris")
        test = self.join_group("          ")
        assert b'joined the group' in test.data
        self.logout()

    def test_join_group_integers(self):
        self.login("Daniel", "Harris")
        test = self.join_group("54321")
        assert b'joined the group' in test.data
        self.logout()

    def test_join_group_symbols(self):
        self.login("Daniel", "Harris")
        test = self.join_group("!!@@##")
        assert b'joined the group' in test.data
        self.logout()


if __name__ == '__main__':

    unittest.main()

