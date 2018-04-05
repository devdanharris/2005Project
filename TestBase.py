import unittest
from GroupProject import *


class TestBase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
        db.create_all()
        self.testApp = app.test_client()
        self.register("Laura", "hunter2")
        self.register("Caleb", "test")

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

    def newPost(self, title, content, topic):
        return self.testApp.post('/new', data=dict(
            title=title,
            content=content,
            topic=topic,
        ), follow_redirects=True)

    def reply(self, content, post_id):
        url = str("/replyto/" + str(post_id))
        return self.testApp.post(url, data=dict(
            content=content
        ), follow_redirects=True)

    def subToPost(self, post_id):
        url = str("/subscribetopost/" + str(post_id))
        return self.testApp.get(url, follow_redirects=True)

    def subToTopic(self, topic):
        url = str("/subscribetotopic/" + str(topic))
        return self.testApp.get(url, follow_redirects=True)

    def testLoggedInPost(self):
        self.login("Laura", "hunter2")
        test = self.newPost("Cast Iron", "How do I season a cast iron skillet?", "Cooking")
        assert b'Post was successfully added' in test.data
        self.logout()

    def testLoggedOutPost(self):
        test = self.newPost("Cast Iron", "How do I season a cast iron skillet?", "Cooking")
        assert b'Error: Must be logged in to post' in test.data

    def testIncompletePost(self):
        self.login("Laura", "hunter2")
        test = self.newPost("Cast Iron", "", "Cooking")
        assert b'Please enter all the fields' in test.data
        self.logout()

    def testReply(self):
        self.login("Laura", "hunter2")
        test = self.reply("Season with non-animal fat and bake", 0)
        assert b'Reply was successfully added' in test.data
        self.logout()

    def testSubscriptions(self):
        self.login("Laura", "hunter2")
        test = self.subToPost(0)
        assert b'subscribed to post' in test.data
        test = self.subToTopic("Cooking")
        assert b'subscribed to topic' in test.data
        self.logout()

    def testDuplicateSubscriptions(self):
        self.login("Laura", "hunter2")
        self.subToPost(0)
        test = self.subToPost(0)
        assert b'already subscribed to post' in test.data
        self.subToTopic("Cooking")
        test = self.subToTopic("Cooking")
        assert b'already subscribed to topic' in test.data
        self.logout()

    def testLoggedOutSubscriptions(self):
        test = self.subToPost(0)
        assert b'Error: Must be logged in to subscribe' in test.data
        test = self.subToTopic("Cooking")
        assert b'Error: Must be logged in to subscribe' in test.data


if __name__ == '__main__':

    unittest.main()