
README

----------------
CONTENTS
----------------
I. FILES INCLUDED
II. PREREQUISITES
III. INSTALLATION
IV. DESCRIPTION
V. INSTRUCTIONS
	i. Registration
	ii. Login
	iii. Post
	iv. Reply
	v. Subscribe to Topic/Post
	vi. View Notifications/Subscriptions
	vii. Create a Group discussion.
	viii. Join a Group discussion.
	ix. Logout
VI. AUTHORS
VII. LICENSE

-------------------------
I. FILES INCLUDED
-------------------------
GroupProject.py          All the classes and methods used to run the prototype.    
TestBase.py 	    Test code to check all of the class methods.
group.html                   HTML template to organize the groups module.
layout.html 	    HTML template to organize the overall layout.
login.html                     HTML template to organize the user login module.
mysubs.html                HTML template to organize the user subscription module.
new.html 		    HTML template to organize the new post module.
register.html                HTML template to organize the user registration module.
reply.html                    HTML template to organize the new reply module.
show_all.html              HTML template to organize the collaberation of all other templates.
style.css		   CSS file to set the HTML template style.

--------------------------
II. PREREQUISITES 
--------------------------
Knowledge of Flask and Virtual Environments is a neccessity.
Set up SQLAlchemy for flask in the venv to use as the database.
(Optional) PyCharm is recommended for using the prototype and will be the program referenced 
for installation guide.

------------------------
III. INSTALLATION
------------------------
1. Unpackage the project.
2. Import GroupProject.py into PyCharm
3. Import templates and static files.
4. Go to File>>Settings>>Project:GroupProject>>Project Interpreter>>Install
5. Search for Flask-SQLAlchemy v2.3.2 (Or later) and install.
6. Installation complete, and can be now be executed. 

-----------------------
IV. DESCRIPTION
------------------------
This prototype is used to create a user discussion forum with features such as: 
User account creation and login, topic/thread posting and replies, subscription and notification, and group discussions.

Built with: Flask - Web framework
	Jinja2 - HTML template engine.
	SQLAlchemy - SQL toolkit and object-relational mapper.

-------------------------
V. INSTRUCTIONS
-------------------------
The following describes how to use the prototype (Note: Some features require that other requirements have been met, specified where applicable.)

	i. Registration:
		1. On the homepage, click the 'Register' hyperlink.	
		2. Enter the fields username, password and confirm password.
		3. Click the 'Register' hyperlink to submit user creation credentials.

	ii. Login:
		(Requires user to be registered, see: Registration)
		1. On the homepage, click the 'Login' hyperlink.
		2. Enter the fields username and password.
		3. Click the 'Login' hyperlink to submit the login request.

	iii. Post:
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'Add Post' hyperlink.
		2. Enter the required fields, title, content and topic.
		3. Click the 'Submit' hyperlink to create the post.

	iv. Reply
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'Replies' hyperlink.
		2. Enter the reply in the designated field.
		3. Click the 'Submit' hyperlink to create the reply.
	
	v. Subscribe to Topic/Post
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'Subscribe to Topic'/'Subscribe to Post' hyperlink. 
   
	vi. View Notifications/Subscriptions
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'My Subscriptions' hyperlink.
		2. (Optional) Click on the subscribed post/topic to view it.
		3. Click the 'Back to Home Page' hyperlink to return to homepage.
	
	vii. Create a Group discussion.
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'Group discussion' hyperlink.
		2. Click 'Create a group' hyperlink.
		3. Enter the required group name.
		4. Click the 'Submit' hyperlink to create the group.
	
	viii. Join a Group discussion
		(Requires user to be logged in, see: Login)
		1. On the homepage, click the 'Group discussion' hyperlink.
		2. Next to the group name, click the 'Join Group' hyperlink.
	 
	ix.	Logout
		1. Click the 'Log out' hyperlink.
	
------------------
VI. AUTHORS
------------------
The prototype referenced by this readme file is created by: Caleb Graves, Sylvia Unimna, Gwang Seop Shin, Daniel Harris
	
-----------------
VII. LICENSE
-----------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


	
   
	
 