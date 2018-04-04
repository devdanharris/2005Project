"""This module is used to create and host a forum for users to login and make topic posts."""

from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy import and_

#Set up the persistent database using SQL Alchemy.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test018.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


class User(db.Model):
    """This User class retrieves the 'Username' and 'Password' of a created account from the database.

        :param id: Identification number assigned to the specific user login credentials determined by linear increment.
        :param username: A name containing up to 15 characters created by the user to be referenced for login and post author identification.
        :param password: A password containing up to 10 characters created by the user to be referenced for login authentication.
        :type id: Integer
        :type username: String
        :type password: String
        :return: Returns null by default upon function success.
    """

    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(15))
    password = db.Column('password', db.String(10))
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post(db.Model):
    """This Post class handles the creation and viewing of new posts, as well as replies to posts.

        :param postID: The identification number to reference an original post, linearly determined.
        :param replyID: The identification number to reference a reply, linearly determined.
        :param title: The user-created name of the post.
        :param content: The user-created body text of the post.
        :param topic: The user created group/topic used to generally identify the post for quick searching.
        :param author: The username of the user who created the post/reply.
        :param replies: The number of replies to an original post.
        :type postID: Integer
        :type replyID: Integer
        :type title: String
        :type content: String
        :type topic: String
        :type author: String
        :type replies: Integer
        :return: Returns null by default upon success.
    """

    __tablename__ = 'post'
    postID = db.Column('post_id', db.Integer, primary_key=True,)
    replyID = db.Column('reply_id', db.Integer)
    title = db.Column(db.String(100))
    content = db.Column(db.String(250))
    topic = db.Column(db.String(20))
    author = db.Column(db.String(15))
    replies = db.Column('replies', db.Integer)
    subscriptions = db.relationship('Subscription', backref='post', lazy=True)

    def __init__(self, title, content, topic, author, replyID = 0):
        self.replyID = replyID
        self.topic = topic
        if replyID is not 0:
            replyto = Post.query.filter_by(postID = replyID).first()
            self.topic = replyto.topic
            replyto.replies = replyto.replies + 1
            subs = Subscription.query.filter(or_(Subscription.postID == replyID,Subscription.topic == replyto.topic))
            for sub in subs:
                sub.notification = True
        self.title = title
        self.content = content
        self.replies = 0
        self.author = author

class Subscription(db.Model):
    """This Subscription class stores all the information of a user's subscriptions to topics and/or posts.

    :param subID: The identification number of the subscription.
    :param userID: The identification number of the user subscribing.
    :param topic: The name of the topic that a user is subscribing to. (Can be None)
    :param postID: The identificiation number of the post that a user is subscribing to.
    :param postTitle: The title of the post that the user is subscribing to.
    :param notification: True or False whether the subscribing user has new notification.
    :type subID: Integer
    :type userID: String
    :type topic: String
    :type postID: Integer
    :type postTitle: String
    :type notification: Boolean
    """


    __tablename__ = 'subscription'
    subID = db.Column('sub_id', db.Integer, primary_key=True)
    userID = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)
    topic = db.Column('topic', db.String(20))
    postID = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    postTitle = db.Column('postTitle', db.String(100))
    notification = db.Column('notification', db.Boolean)

    def __init__(self, user, topic, postID = 0):
        self.userID = user
        self.topic = topic
        self.postID = postID
        if postID is not 0:
            self.postTitle = Post.query.filter_by(postID=postID).first().title
        self.notification = False

class Group(db.Model):
    """This Group class stores all the information about a user created group. Including the group name, and the creator.

    :param groupID: The identification number of the group.
    :param userID: The identification number of the user referencing the group.
    :param group_name: The name of the group, defined by the creator.
    :type groupID: Integer
    :type userID: Integer
    :type group_name: String
    """

    __tablename__ = 'group'
    groupID = db.Column('group_id', db.Integer, primary_key=True)
    userID = db.Column(db.String(15), db.ForeignKey('user.id'), nullable=False)
    group_name = db.Column('group_name', db.String(20))

    def __init__(self, group_name, groupID = 0):
        self.group_name = group_name
        self.groupID = groupID
        if session.get('username'):
            self.userID = session['username']


@app.route('/new', methods=['GET', 'POST'])
def new():
    """Creates a new post with a title, content and topic

    :return: Returns the HTML template 'new.html'.
    """
    # Check to see if the user is logged into an existing account.
    if request.method == 'POST':
        if session.get('username') is None:
            flash('Error: Must be logged in to post')
        # Deny the post with an error flashed if the content area is left blank.
        elif not request.form['title' ] or not request.form['content']:

            flash('Please enter all the fields', 'error')
        # Otherwise, create a post with the entered title, content, topic, and the author's username.
        else:
            post = Post(request.form['title'], request.form['content'], request.form['topic'], session['username'])
            # Loop through the subscriptions to notify the users (who are subscribed) that a new post has been made.
            subs = Subscription.query.filter(Subscription.topic == request.form['topic'])
            for sub in subs:
                sub.notification = True
            # Commit the post to the database to be stored.
            db.session.add(post)
            db.session.commit()
            # Notify success to the user and redirect to the home page.
            flash('Post was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/replyto/<int:post_id>', methods=['GET', 'POST'])
def replyto(post_id):
    """Creates a reply to the post referenced by the original post ID.

    :param post_id: The ID number of the original post to be replied to.
    :type post_id: Integer
    :return: Returns the HTML template 'reply.html'.
    """
    # Check to see if the user is logged into an existing account.
    if request.method == 'POST':
        if session.get('username') is None:
            flash('Error: Must be logged in to post')
        # Deny the post with an error flashed if the content area is left blank.
        elif not request.form['content']:
            flash('Please enter a reply between 1 and 250 characters', 'error')
        # Otherwise, create the reply to the post identified by post_id with the content, and the author's username.
        else:
            post = Post("Reply", request.form['content'], " ", session['username'], post_id)
            # Commit the reply to the database to be stored.
            db.session.add(post)
            db.session.commit()
            # Notify success to the user and redirect to the home page.
            flash('Reply was successfully added')
            return redirect(url_for('show_all'))
    return render_template('reply.html', posts=Post.query.filter(or_(Post.replyID == post_id, Post.postID == post_id)))

@app.route('/subscribetotopic/<topic>')
def subscribetotopic(topic):
    """Subscribes the user to their selected topic keyword.

    :param topic: The topic name to be referenced when checking for notifications.
    :type topic: String
    :return: Returns the HTML template 'show_all.html'.
    """
    # Check to see if the user is logged into an existing account.
    if session.get('username') is None:
        flash('Error: Must be logged in to subscribe')
    # Add the subscription to the topic name for the user currently logged in.
    elif Subscription.query.filter(and_(Subscription.topic == topic, Subscription.userID == session['username'])).first() is None:
        sub = Subscription(session['username'], topic)
        # Commit the subscription to the database.
        db.session.add(sub)
        db.session.commit()
        # Notify success to the user and redirect to the home page.
        flash(str(session['username']) + " subscribed to topic " + topic)
    else:
        # If the user is already subscribed to the topic requested, flash the following notification.
        flash("You're already subscribed to topic " + topic)
    return redirect(url_for('show_all'))

@app.route('/subscribetopost/<int:post_id>')
def subscribetopost(post_id):
    """Subscribes the user to their selected post keyword.

    :param post_id: The post id to be referenced when checking for notifications.
    :type post_id: Integer
    :return: Returns the HTML template 'show_all.html'.
    """
    # Check to see if the user is logged into an existing account.
    if session.get('username') is None:
        flash('Error: Must be logged in to subscribe')
    # Add the subscription to the post name for the user currently logged in.
    elif Subscription.query.filter(and_(Subscription.postID == post_id, Subscription.userID == session['username'])).first() is None:
        sub = Subscription(session['username'], None, post_id)
        # Commit the subscription to the database.
        db.session.add(sub)
        db.session.commit()
        # Notify success to the user and redirect to the home page.
        flash(str(session['username']) + " subscribed to post " + str(post_id))
    else:
        # If the user is already subscribed to the post requested, flash the following notification.
        flash("You're already subscribed to post " + str(post_id))
    return redirect(url_for('show_all'))

@app.route('/mysubs')
def showSubs():
    """Generates a list of all subscriptions that a user has made.

    :return: Returns the HTML template 'mysubs.html'.
    """
    # Check to see if the user is logged into an existing account.
    if session.get('username') is None:
        flash('Error: Must be logged in to view subscriptions')
    else:
        # Check and gather the subscriptions that the user has made.
        subs = Subscription.query.filter(Subscription.userID == session['username'])
        # Show the current user's subscriptions.
        x = render_template('mysubs.html', subTopics=Subscription.query.filter(and_(Subscription.userID == session['username'], Subscription.postID == 0)), subPosts=db.session.query(Subscription).filter(and_(Subscription.userID == session['username'], (Subscription.topic == None))))
        # Set the user's notifications to false (since they have been checked once this code is executed).
        for sub in subs:
            sub.notification = False
        # Update the database and commit.
        db.session.commit()
        return x

@app.route('/topic/<topic>')
def showTopic(topic):
    """Creates a compilation of all the templates to view the overall project with topics included.

    :param topic: The topic to be added to the page.
    :type topic: String
    :return: Returns the HTML template 'show_all.html'.
    """
    # Renders the show all template.
    return render_template('show_all.html', posts=Post.query.filter(and_(Post.replyID == 0, Post.topic == topic)))

@app.route('/')
def show_all():
    """Creates a compilation of all templates to view the overall project.

    :return: Returns the HTML template 'show_all.html'.
    """
    # Renders the show all template.
    return render_template('show_all.html', posts=Post.query.filter(Post.replyID == 0), groups=Group.query.filter(Group.groupID == 0))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Checks the user login credentials to authenticate the login attempt.

    :return: Returns the redirect url for 'show_all.html' if successfully logged in;
             Returns the redirect url for 'login.html' if unsuccessful login attempt;
             Returns the HTML template 'login.html' if an error occurred.
    """
    error = None
    if request.method == 'POST':
        # Request and store the entered username if it exists.
        loginuser = User.query.filter_by(username = request.form['username']).first()
        if loginuser:
            # Check if the entered password matches the password stored for the username.
            if loginuser.password == request.form['password']:
                    # If the password matches, set the session user to 'username' and toggle logged in to true.
                    session['username'] = request.form['username']
                    session['logged_in'] = True
                    # Notify the user that they were successfully logged in.
                    flash('You were logged in as ' + session['username'])

                    return redirect(url_for('show_all'))
            # With incorrect password, notify the user that an error has been made.
            else:
                flash('Incorrect Username and/or Password')
                # Reload the login page.
                return redirect(url_for('login'))
        # With incorrect username, notify the user that an error has been made.
        else:
            flash('Incorrect Username and/or Password')
            # Reload the login page.
            return render_template('login.html')
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Creates a new user object with a unique username and password.

    :return: Returns the redirect url for 'show_all.html' if successfully registered;
             Returns the redirect url for 'register.html' if unsuccessful register attempt;
             Returns the HTML template 'register.html' if an error occurred.
    """
    error = None
    if request.method == 'POST':
        # Check if the user attempting to register has left any fields blank.
        if not request.form['username'] or not request.form['password']:
            # Notify the user that fields have been left blank and reload the page.
            flash('Please enter all the fields')
            render_template('register.html')
        else:
            # Check if the entered username exists.
            loginuser = User.query.filter_by(username=request.form['username']).first()
            # If the username entered is unique, proceed to create the account.
            if not loginuser:
                # Create the user with the entered username and password.
                user = User(request.form['username'], request.form['password'])
                # Commit the user to the database and store it.
                db.session.add(user)
                db.session.commit()
                # Notify the user of successful account creation.
                flash('User Successfully Registered')
                return redirect(url_for('show_all'))
            # If the username exists, flash the error and reload the page.
            else:
                flash('Error: User already exists')
                return redirect(url_for('register'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs out the current user from the session.

    :return: Returns the redirect url for 'show_all.html'.
    """
    # Set logged in to none (false) and username to none.
    session.pop('logged_in', None)
    session.pop('username', None)
    # Notify the user of logout success and reload the page.
    flash('You were logged out')
    return redirect(url_for('show_all'))

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    """Creates a group with the defined group name, and logs the creator.

    :return: Returns the redirect url for 'show_all.html' upon successful group creation.
    """

    error = None
    if request.method == 'POST':
        # Check to see if the user is logged in, flash the error if not.
        if session.get('username') is None:
            flash('Error: Must be logged in to create a group.')
        # Check to see if the user entered a name for the group in the required field, flash the error if not.
        if not request.form['group_name']:
            flash('Please enter the group name.')
            render_template('group.html')
        else:
            # Set the group name to the name entered by the user.
            group_name = Group.query.filter_by(group_name=request.form['group_name']).first()
            # If the group does not already exist, create the group with the user entered name.
            if not group_name:
                group = Group(request.form['group_name'])
                # Commit the group to the database and store it.
                db.session.add(group)
                db.session.commit()
                # Notify the user that the group was created successfully.
                flash('Group Successfully Created')
                return redirect(url_for('show_all'))
            # If the group exists already, flash the error and reload the page.
            else:
                flash('Error: Group already exists')
                return redirect(url_for('create_group'))
    return render_template('group.html', error=error)

@app.route('/join_group/<group_name>')
def join_group(group_name):
    """Allows a user to join a group.

    :param group_name: The name of the group for the user to join.
    :type group_name: String.
    :return: Returns the redirect url for 'show_all.html'.
    """

    # Check if the user is logged in, flash the error if not.
    if session.get('username') is None:
        flash('Error: Must be logged in to join a group')
    # Add the current user to the group specified by group_name.
    elif Group.query.filter(and_(Group.group_name == group_name, Group.userID == session['username'])).first() is None:     #[SQL: 'INSERT INTO "group" (group_id, "userID", group_name) VALUES (?, ?, ?)'] [parameters: ('fgh', 'assd', 'assd')]  , Group.userID == session['username'] and_(Group.group_name == group_name, Group.userID == session['username'])
        group = Group(session['username'], group_name)  #Im passing in a username here, but not accepting it in the Group() parameters. Fix this.
        # Commit the user to the group and store.
        db.session.add(group)
        db.session.commit()
        # Notify the user of the successful join to the group.
        flash(str(session['username']) + " joined the group " + group_name)
    # If the user is already in the group, flash the error.
    else:
        flash("You're already a member of the group " + group_name)
    return redirect(url_for('show_all'))


db.create_all()
if __name__ == '__main__':

    app.run()



