Fall Risk DB
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Running the development server
++++++++++++++++++++++++++++++

Using the development server is an easy process. First, you will need to clone the repository and change your directory to the root of the project.

::
    
    $ git clone git@github.com:RIT-MSD-P21015/fall_risk_db.git
    $ cd fall_risk_db

Next, we will install our virtual environment. This project requires that you have Python 3 installed on your system.

::
    
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

Now we are ready to run the web server. Next, open up another terminal, change the working directory to the root of the git repository, and activate the virtual environment we just created. Now we are ready to run the development server. In the same terminal, run ``make dev``. You should now see that the server is up and running at ``http://0.0.0.0:5000`` and ready to accept connections. Leave this terminal open, as it will contain useful debugging information regarding the server. In another terminal, navigate to the root the git repository and notice the new sqlite database that has been created called ``db.sqlite3``. You can use a database viewer such as the one `here <https://sqlitebrowser.org/>`_ to view the database in real time.

Next, with the development server still up an running, we will seed the database with an administrator account. Using a new terminal, change the working directory to the root of the git repository and activate the virtual environment. Enter the following commands into your shell with the ``<firstname>``, ``<lastname>``, ``<email>``, and ``<password>`` fields replaced with the values of your choice for the admin account.

::
    
    $ export FLASK_APP=fall_risk_db.py
    $ flask create-admin <firstname> <lastname> <email> <password>

Now the web server is ready to be used. Alternatively, you can open up a special Python shell to interact in real time with the application using ``flask shell``. Note that when you shut down the server, the ``db.sqlite3`` database file will still persist, and will be used on the next start up.

The authentication process
++++++++++++++++++++++++++

In order to use the REST API, the user must create an account using the ``POST /api/user`` endpoint. Admin accounts must be created manually as described in the previous section. Once the account has been created the first step is to get a temporary access token using the ``POST /api/tokens`` endpoint. In this request, the email and password of the user account must be included in the HTTP header as shown below. This protocol is referred to as `Basic Authentication <https://datatracker.ietf.org/doc/html/rfc7617>`_.

::
    
    Authorization: Basic <credentials>

Note that ``credentials`` is the base64 encoded version of the colon separated string ``email:password``. Once this request is made, you will now have access to your temporary access token. This token is linked back to your account so when you use in an API request, it will return or modify data from your account. To use the token in an API request, you will need encode this in your HTTP header as shown below. This protocol is referred to as `Bearer Authentication <https://datatracker.ietf.org/doc/html/rfc6750>`_.

::

    Authorization: Bearer <token>

This should be all you need to get going. See the source code documentation for more details about the REST API.

Source Code
===========

User Model
++++++++++

.. autoclass:: app.models.User
   :members:
   :show-inheritance:

REST API Endpoints
++++++++++++++++++

User
----

.. automodule:: app.api.user
   :members:

Admin
-----

.. automodule:: app.api.admin
   :members:

Tokens
------

.. automodule:: app.api.tokens
   :members:


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
