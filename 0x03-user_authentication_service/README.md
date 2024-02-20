<h1>0x03-user_authentication_service</h1>
<img src='img/authentication.jpg'>

<p>In the industry, you should not implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: <a href="https://intranet.alxswe.com/rltoken/9nVfotMI_1zpEzihMzBeTA">Flask-User</a>). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.
</p>
<h1>Resources</h1>

<li><a href="https://intranet.alxswe.com/rltoken/lKExyvivrrW4eh0eI8UV6A">Flask documentation</a></li>
<li><a href="https://intranet.alxswe.com/rltoken/py7LuuD1u2MUwcaf8wnDzQ">Requests module</a></li>
<li><a href="https://intranet.alxswe.com/rltoken/cj-mc5ZHp_KyXn1yikHC0A">HTTP status codes</a></li>

<h1>Setup</h1>
<p>You will need to install bcrypt</p>
<pre>
pip3 install bcrypt
</pre><br>
<h1>Tasks</h1>
<b>0. User model</b>
<p>
In this task you will create a SQLAlchemy model named User for a database table named users (by using the <a href="https://intranet.alxswe.com/rltoken/-a69l-rGqoFdXnnu6qfKdA">mapping declaration</a> of SQLAlchemy).
</p>
<p>
The model will have the following attributes:
</p>
<li>id, the integer primary key</li>
<li>email, a non-nullable string</li>
<li>hashed_password, a non-nullable string</li>
<li>session_id, a nullable string</li>
<li>reset_token, a nullable string</li>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

bob@dylan:~$ python3 main.py
users
users.id: INTEGER
users.email: VARCHAR(250)
users.hashed_password: VARCHAR(250)
users.session_id: VARCHAR(250)
users.reset_token: VARCHAR(250)
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: user.py</li>
   
<b>1. create user</b>
<p>
In this task, you will complete the DB class provided below to implement the add_user method.
</p>
<pre>
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

</pre>
<p>
Note that DB._session is a private property and hence should NEVER be used from outside the DB class.
</p>
<p>
Implement the add_user method, which has two required string arguments: email and hashed_password, and returns a User object. The method should save the user to the database. No validations are required at this stage.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

bob@dylan:~$ python3 main.py
1
2
bob@dylan:~$
</pre><br>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: db.py</li>
   
<b>2. Find user</b>
<p>
In this task you will implement the DB.find_user_by method. This method takes in arbitrary keyword arguments and returns the first row found in the users table as filtered by the method’s input arguments. No validation of input arguments required at this point.
</p>
<p>
Make sure that SQLAlchemy’s NoResultFound and InvalidRequestError are raised when no results are found, or when wrong query arguments are passed, respectively.
</p>
<b>Warning:</b>

<li>NoResultFound has been moved from sqlalchemy.orm.exc to sqlalchemy.exc between the version 1.3.x and 1.4.x of SQLAchemy - please make sure you are importing it from sqlalchemy.orm.exc
</li>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")        

bob@dylan:~$ python3 main.py
1
1
Not found
Invalid
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: db.py</li>
   
<b>3. update user</b>
<p>
In this task, you will implement the DB.update_user method that takes as argument a required user_id integer and arbitrary keyword arguments, and returns None.
</p>
<p>
The method will use find_user_by to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.
</p>
<p>
If an argument that does not correspond to a user attribute is passed, raise a ValueError.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

bob@dylan:~$ python3 main.py
1
Password updated
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: db.py</li>
   
<b>4. Hash password</b>
<p>
In this task you will define a _hash_password method that takes in a password string arguments and returns bytes.</p>
<p>
The returned bytes is a salted hash of the input password, hashed with bcrypt.hashpw.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import _hash_password

print(_hash_password("Hello Holberton"))

bob@dylan:~$ python3 main.py
b'$2b$12$eUDdeuBtrD41c8dXvzh95ehsWYCCAi4VH1JbESzgbgZT.eMMzi.G2'
bob@dylan:~$
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>5. Register user</b>
<p>
In this task, you will implement the Auth.register_user in the Auth class provided below:
</p>
<pre>
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

</pre>
<p>
Note that Auth._db is a private property and should NEVER be used from outside the class.
</p>
<p>
Auth.register_user should take mandatory email and password string arguments and return a User object.
</p>
<p>
If a user already exist with the passed email, raise a ValueError with the message User <user's email> already exists.
</p>
<p>
If not, hash the password with _hash_password, save the user to the database using self._db and return the User object.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'me@me.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))        

bob@dylan:~$ python3 main.py
successfully created a new user!
could not create a new user: User me@me.com already exists
bob@dylan:~$
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>6. Basic Flask app</b>
<p>
In this task, you will set up a basic Flask app.
</p>
<p>
Create a Flask app that has a single GET route ("/") and use flask.jsonify to return a JSON payload of the form:
</p>
<pre>

{"message": "Bienvenue"}
Add the following code at the end of the module:

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>7. Register user</b>
<p>
In this task, you will implement the end-point to register a user. Define a users function that implements the POST /users route.
</p>
<p>
Import the Auth object and instantiate it at the root of the module as such:
</p>
<pre>
from auth import Auth


AUTH = Auth()
</pre>
<p>
The end-point should expect two form data fields: "email" and "password". If the user does not exist, the end-point should register it and respond with the following JSON payload:
</p>
<pre>
{"email": "<registered email>", "message": "user created"}
</pre>
<p>
If the user is already registered, catch the exception and return a JSON payload of the form
</p>
<pre>
{"message": "email already registered"}
</pre>
<p>
and return a 400 status code
</p>
<p>
Remember that you should only use AUTH in this app. DB is a lower abstraction that is proxied by Auth.
</p>
Terminal 1:
<pre>
bob@dylan:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
</pre>
Terminal 2:
<pre>
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 52
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:18 GMT
< 
{"email":"bob@me.com","message":"user created"}

bob@dylan:~$
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 400 BAD REQUEST
< Content-Type: application/json
< Content-Length: 39
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:33 GMT
< 
{"message":"email already registered"}
bob@dylan:~$
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>8. Credentials validation</b>
<p>
In this task, you will implement the Auth.valid_login method. It should expect email and password required arguments and return a boolean.
</p>
<p>
Try locating the user by email. If it exists, check the password with bcrypt.checkpw. If it matches return True. In any other case, return False.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

bob@dylan:~$ python3 main.py
True
False
False
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>9. Generate UUIDs</b>
<p>
In this task you will implement a _generate_uuid function in the auth module. The function should return a string representation of a new UUID. Use the uuid module.
</p>
<p>
Note that the method is private to the auth module and should NOT be used outside of it.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>10. Get session ID</b>
<p>
In this task, you will implement the Auth.create_session method. It takes an email string argument and returns the session ID as a string.
</p>
<p>
The method should find the user corresponding to the email, generate a new UUID and store it in the database as the user’s session_id, then return the session ID.
</p>
<p>
Remember that only public methods of self._db can be used.
</p>
<pre>
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

bob@dylan:~$ python3 main.py
5a006849-343e-4a48-ba4e-bbd523fcca58
None
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>11. Log in</b>
<p>
In this task, you will implement a login function to respond to the POST /sessions route.
</p>
<p>
The request is expected to contain form data with "email" and a "password" fields.
</p>
<p>
If the login information is incorrect, use flask.abort to respond with a 401 HTTP status.
</p>
<p>
Otherwise, create a new session for the user, store it the session ID as a cookie with key "session_id" on the response and return a JSON payload of the form
</p>
<pre>
{"email": "<user email>", "message": "logged in"}
</pre>
<pre>
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
{"email":"bob@bob.com","message":"user created"}
bob@dylan:~$ 
bob@dylan:~$  curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=163fe508-19a2-48ed-a7c8-d9c6e56fabd1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:34 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
bob@dylan:~$ 
bob@dylan:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=BlaBla' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 34
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 34 out of 34 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: text/html; charset=utf-8
< Content-Length: 338
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:45 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
* Closing connection 0
bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>12. Find user by session ID</b>
<p>
In this task, you will implement the Auth.get_user_from_session_id method. It takes a single session_id string argument and returns the corresponding User or None.
</p>
<p>
If the session ID is None or no user is found, return None. Otherwise return the corresponding user.
</p>
<p>
Remember to only use public methods of self._db.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>13. Destroy session</b>
<p>
In this task, you will implement Auth.destroy_session. The method takes a single user_id integer argument and returns None.
</p>
<p>
The method updates the corresponding user’s session ID to None.
</p>
<p>
Remember to only use public methods of self._db.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>14. Log out</b>
<p>
In this task, you will implement a logout function to respond to the DELETE /sessions route.
</p>
<p>
The request is expected to contain the session ID as a cookie with key "session_id".
</p>
<p>
Find the user with the requested session ID. If the user exists destroy the session and redirect the user to GET /. If the user does not exist, respond with a 403 HTTP status.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>15. User profile</b>
<p>
In this task, you will implement a profile function to respond to the GET /profile route.
</p>
<p>
The request is expected to contain a session_id cookie. Use it to find the user. If the user exist, respond with a 200 HTTP status and the following JSON payload:
</p>
<pre>
{"email": "<user email>"}
</pre>
<p>
If the session ID is invalid or the user does not exist, respond with a 403 HTTP status.
</p>
<pre>
bob@dylan:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=75c89af8-1729-44d9-a592-41b5e59de9a1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:15:57 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
bob@dylan:~$
bob@dylan:~$ curl -XGET localhost:5000/profile -b "session_id=75c89af8-1729-44d9-a592-41b5e59de9a1"
{"email": "bob@bob.com"}
bob@dylan:~$ 
bob@dylan:~$ curl -XGET localhost:5000/profile -b "session_id=nope" -v
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /profile HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Cookie: session_id=75c89af8-1729-44d9-a592-41b5e59de9a
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: text/html; charset=utf-8
< Content-Length: 234
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:16:43 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>403 Forbidden</title>
<h1>Forbidden</h1>
<p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>
* Closing connection 0

bob@dylan:~$ 
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>16. Generate reset password token</b>
<p>
In this task, you will implement the Auth.get_reset_password_token method. It take an email string argument and returns a string.
</p>
<p>
Find the user corresponding to the email. If the user does not exist, raise a ValueError exception. If it exists, generate a UUID and update the user’s reset_token database field. Return the token.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>17. Get reset password token</b>
<p>
In this task, you will implement a get_reset_password_token function to respond to the POST /reset_password route.
</p>
<p>
The request is expected to contain form data with the "email" field.
</p>
<p>
If the email is not registered, respond with a 403 status code. Otherwise, generate a token and respond with a 200 HTTP status and the following JSON payload:
</p>
<pre>
{"email": "<user email>", "reset_token": "<reset token>"}
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>18. Update password</b>
<p>
In this task, you will implement the Auth.update_password method. It takes reset_token string argument and a password string argument and returns None.
</p>
<p>
Use the reset_token to find the corresponding user. If it does not exist, raise a ValueError exception.
</p>
<p>
Otherwise, hash the password and update the user’s hashed_password field with the new hashed password and the reset_token field to None.
</p>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: auth.py</li>
   
<b>19. Update password end-point</b>
<p>
In this task you will implement the update_password function in the app module to respond to the PUT /reset_password route.
</p>
<p>
The request is expected to contain form data with fields "email", "reset_token" and "new_password".
</p>
<p>
Update the password. If the token is invalid, catch the exception and respond with a 403 HTTP code.
</p>
<p>
If the token is valid, respond with a 200 HTTP code and the following JSON payload:
</p>
<pre>
{"email": "<user email>", "message": "Password updated"}
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: app.py</li>
   
<b>20. End-to-end integration test</b>
<p>
Start your app. Open a new terminal window.
</p>
<p>
Create a new module called main.py. Create one function for each of the following tasks. Use the requests module to query your web server for the corresponding end-point. Use assert to validate the response’s expected status code and payload (if any) for each task.
</p>
<li>register_user(email: str, password: str) -> None</li>
<li>log_in_wrong_password(email: str, password: str) -> None</li>
<li>log_in(email: str, password: str) -> str</li>
<li>profile_unlogged() -> None</li>
<li>profile_logged(session_id: str) -> None</li>
<li>log_out(session_id: str) -> None</li>
<li>reset_password_token(email: str) -> str</li>
<li>update_password(email: str, reset_token: str, new_password: str) -> None</li>
<p>
Then copy the following code at the end of the main module:
</p>
<pre>
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
Run python main.py. If everything is correct, you should see no output.
</pre>
<b>Repo:</b>

<li>GitHub repository: alx-backend-user-data</li>
<li>Directory: 0x03-user_authentication_service</li>
<li>File: main.py</li>