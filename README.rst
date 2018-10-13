Foosball API Service
====================

*A Foosball API REST Service*

**Note:** This project is not for production for a few reasons:

1. The intent of this project is for review, not production.

2. The project uses the Python wsgiref server which is good for local
running and testing but nothing more.

3. The project uses global variables to hold the game state, normally
this would be delegated to something like MongoDB, Postgres, etc.

This project was tested and built using Python 3.6.6.

Running the tests
^^^^^^^^^^^^^^^^^^^

**Note:** It was not required to write tests for this project. Regardless,
a few tests have been added.

You can run the tests either with ``tox``:

::

    tox

Or with ``nosetests``:

::

    nosetests

Make sure to install the test dependencies.


Running the Project
^^^^^^^^^^^^^^^^^^^

You can run this the normal Python way or install it. From the main
project folder run:

::

    pip install -e .

Then run:

::

    foosball

You should see the server start on ``127.0.0.1:8080``

The API and cURL Commands
^^^^^^^^^^^^^^^^^^^^^^^^^

There are several supported API calls. In this section I will supply readers with
each command was well as the expected results (results vary on the
data that has been fed in).

**Register a new user:**

This call will create a new player along with a specified table. If the
name already exists that named player is adjusted to any table changes you
give thus supporting returning player calls to switch between tables or
create new tables.

If the table already exists you will be joined to it if there is one other
player. If there are two players this forces the current game to be abandoned
and the new player will be the only one at the table.

JSON Schema enforced.

**REQUIRED** ``name`` limited between 4 and 15 characters

**REQUIRED** ``table`` is an integer with a minimum value of 1

**REQUIRED** ``color`` player color, must be either yellow or black

::

    curl -X POST http://127.0.0.1:8080/api/v1/registration -v -d '{"name": "test1", "color": "black", "table": 100}' -H "Content-Type: application/json" -H "Accept: application/json"

**Response:**

**HTTP/1.0 201 Created**

::

    {"status": "WAITING"}

There are three status values: WAITING, COMPLETED, STARTED

**Record a goal:**

This call will record a goal (score) from a player to a game table (in-progress games).

If the table already exists you will be joined to it if there is one other
player. If there are two players this forces the current game to be abandoned
and the new player will be the only one at the player's table.

**REQUIRED** ``table`` is an integer with a minimum value of 1

**REQUIRED** ``color`` player color, must be either yellow or black

::

    curl -X POST http://127.0.0.1:8080/api/v1/goal -v -d '{"color": "black", "table": 101}' -H "Content-Type: application/json" -H "Accept: application/json"

**Response:**

**HTTP/1.0 200 OK**

::

    {"status": "STARTED", "yellow_score": 0, "black_score": 1}

**Get the status of a (game) table:**

This call retrieves the specified (if it exists) table's status.

**REQUIRED** ``table_num`` an integer for a specific table

The example below uses the value 200 for the ``table_num``.

::

    curl -X GET http://127.0.0.1:8080/api/v1/table/200 -v -H "Content-Type: application/json" -H "Accept: application/json"

**Response:**

**HTTP/1.0 200 OK**

::

    {"status": "WAITING"}


**Getting a player's win/loss record:**

This call retrieves the specified (if it exists) player's win/loss record.

**REQUIRED** ``table_num`` limited between 4 and 15 characters

The example below uses the value 200 for the ``table_num``.

::

    curl -X GET http://127.0.0.1:8080/api/v1/table/200 -v -H "Content-Type: application/json" -H "Accept: application/json"

**Response:**

**HTTP/1.0 200 OK**

::

    [{"winner": "test3", "winner_score": 5, "opponent": "test1", "opponent_score": 1,
    "datetime_completed": "2018-10-12 22:09:05", "table_num": 100}, {"winner": "test2",
    "winner_score": 5, "opponent": "test1", "opponent_score": 1,
    "datetime_completed": "2018-10-12 22:13:36", "table_num": 101}]

**Get the version:**

This call will fetch the version number of the service.

::

    curl -X POST http://127.0.0.1:8080/api/v1/version -v

**Response:**

**HTTP/1.0 200 OK**

::

    {"version": "1.0.0"}
