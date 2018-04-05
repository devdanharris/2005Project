import unittest
from GroupProject import *


class TestUsers(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
        db.create_all()
        self.testApp = app.test_client()
        self.register("Daniel", "Harris")
        self.register("Different", "User")
        self.register("~!@#$", "%^&*")
        self.register("1234", "5678")
        self.register("waytoomanycharactersinthisline", "waytoomanycharactersinthisline")

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

    def test_register_common(self):
        test = self.register("Winter", "Semester")
        assert b'User Successfully Registered' in test.data

    @unittest.expectedFailure
    def test_register_null(self):
        test = self.register("", "")
        assert b'Please enter all the fields' in test.data

    @unittest.expectedFailure
    def test_register_null_name(self):
        test = self.register("", "pass")
        assert b'Please enter all the fields' in test.data

    @unittest.expectedFailure
    def test_register_null_password(self):
        test = self.register("name", "")
        assert b'User Successfully Registered' in test.data

    @unittest.expectedFailure
    def test_register_duplicate(self):
        self.register("Dupe", "licate")
        test = self.register("Dupe", "licate")
        assert b'User Successfully Registered' in test.data

    @unittest.expectedFailure
    def test_register_duplicate_name(self):
        self.register("Duplicate", "one")
        test = self.register("Duplicate", "two")
        assert b'User Successfully Registered' in test.data

    def test_register_duplicate_pass(self):
        self.register("First", "duplicate")
        test = self.register("Second", "duplicate")
        assert b'User Successfully Registered' in test.data

    def test_register_whitespace(self):
        test = self.register("   ", "   ")
        assert b'User Successfully Registered' in test.data

    def test_register_symbols(self):
        test = self.register("~!@#$%^&*()_+", "{}:<>?-=[];',./")
        assert b'User Successfully Registered' in test.data

    def test_register_integers(self):
        test = self.register("0123", "4567")
        assert b'User Successfully Registered' in test.data

    def test_register_over_character_limit(self):
        test = self.register("toomanycharactersinthisline", "toomanycharactersinthisline")
        assert b'User Successfully Registered' in test.data

    def test_logout(self):
        self.login("Daniel", "Harris")
        test = self.logout()
        assert b'You were logged out' in test.data

    def test_login_common(self):
        test = self.login("Daniel", "Harris")
        assert b'You were logged in as ' in test.data
        self.logout()

    @unittest.expectedFailure
    def test_login_null(self):
        test = self.login("", "")
        assert b'You were logged in as ' in test.data
        #self.logout()  # Might have to remove this for errors.

    @unittest.expectedFailure
    def test_login_null_name(self):
        test = self.login("", "Harris")
        assert b'You were logged in as ' in test.data
       # self.logout()  # Might have to remove this for errors.

    @unittest.expectedFailure
    def test_login_null_password(self):
        test = self.login("Daniel", "")
        assert b'You were logged in as ' in test.data
       # self.logout()  # Might have to remove this for errors.

    @unittest.expectedFailure
    def test_login_case_sensitive_name(self):
        test = self.login("dANIEL", "Harris")
        assert b'You were logged in as ' in test.data
      #  self.logout()  # Might have to remove this for errors

    @unittest.expectedFailure
    def test_login_case_sensitive_pass(self):
        test = self.login("Daniel", "hARRIS")
        assert b'You were logged in as ' in test.data
     #   self.logout()  # Might have to remove this for errors

    @unittest.expectedFailure
    def test_login_whitespace_after_name(self):
        test = self.login("Daniel   ", "Harris")
        assert b'You were logged in as ' in test.data
    #    self.logout()  # Might have to remove this for errors

    @unittest.expectedFailure
    def test_login_whitespace_before_name(self):
        test = self.login("   Daniel", "Harris")
        assert b'You were logged in as ' in test.data
     #   self.logout()  # Might have to remove this for errors

    @unittest.expectedFailure
    def test_login_whitespace_after_password(self):
        test = self.login("Daniel", "Harris   ")
        assert b'You were logged in as ' in test.data
    #    self.logout()  # Might have to remove this for errors

    @unittest.expectedFailure
    def test_login_whitespace_before_password(self):
        test = self.login("Daniel", "   Harris")
        assert b'You were logged in as ' in test.data
     #   self.logout()  # Might have to remove this for errors

    def test_login_symbols(self):
        test = self.login("~!@#$", "%^&*")
        assert b'You were logged in as ' in test.data
        self.logout()

    def test_login_integers(self):
        test = self.login("1234", "5678")
        assert b'You were logged in as ' in test.data
        self.logout()

    def test_login_over_character_limit(self):
        test = self.login("waytoomanycharactersinthisline", "waytoomanycharactersinthisline")
        assert b'You were logged in as ' in test.data
        self.logout()

    def test_duplicate_login_same_user(self):
        self.login("Daniel", "Harris")
        test = self.login("Daniel", "Harris")
        assert b'You were logged in as ' in test.data
        self.logout()

    def test_duplicate_login_different_user(self):
        self.login("Different", "User")
        test = self.login("Daniel", "Harris")
        assert b'You were logged in as ' in test.data
        self.logout()

    def test_logout_not_logged_in(self):
        test = self.logout()
        assert b'You were logged out' in test.data

if __name__ == '__main__':

    unittest.main()

