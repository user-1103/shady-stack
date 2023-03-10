.. SHADY-STACK documentation master file, created by
   sphinx-quickstart on Tue Mar  7 16:35:16 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _repo: https://github.com/user-1103/shady-stack

.. _nix: https://nixos.org/

.. _poetry: https://python-poetry.org/docs/

.. _JSON: https://docs.python.org/3/library/json.html

.. _flask: https://flask.palletsprojects.com/en/2.2.x/

.. _wraper:  https://www.geeksforgeeks.org/function-wrappers-in-python/

Welcome to SHADY-STACK
======================

Overview
````````
Before we dive into the code, lets talk about the abstract concepts.

What Is SHADY-STACK?
-------------------

As the name implies, this is a less than kosher web stack based of the SWAG
stack. I developed it for my projects as I am in university and web hosting can
be expensive. The shady stack consists of the following:

1. A **S** tatic site hosted (GitHub Pages, GitLab Pages, etc.) 
2. Simplistic pages that communicate to the backend via a already existing web-app's Web
   **H** ooks (Slack, Discord, Gsuit, GitHub Actions, etc.).  
3. An **A** plication Bridge program that can read the calls to the webhooks and
   pass them to the next component. 
4. A Backend **D** eamon that acutely presses the requests from the webhooks and
   updates a local copy of the site tree as needed.  
5. An application that regularly s **Y** ncs the local tree
   with the remote tree served as the static site in step 1.

What Is This?
-------------

In this webpage you will find the documentation for using the SHADY-STACK.

.. note::

    This sample documentation was generated on |today|, and is rebuilt with
    each release.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Is SHADY-STACK Right For You?
-----------------------------

There are some ups and downs to using this stack.

+--------------------------------+----------------------------------+
| Pros                           | Cons                             |
+================================+==================================+
| Backend is hidden behind a     | Failure or delay in the webhook  |
| proxy of sorts.                | provider means failure/delay     |
|                                | in your site.                    |
+--------------------------------+----------------------------------+
| It's free!                     | Depending on the web hook        |
|                                | provider, it may be breaking a   |
|                                | TOS or two.                      |
+--------------------------------+----------------------------------+
| It's kinda fail-safe.          | The number of components between |
| If the backend breaks,         | your frontend and backend means  |
| the static parts of your       | it's slow to update.             |
| site will still work.          |                                  |
+--------------------------------+----------------------------------+

Remember to consult your physician to see if SHADY-STACK is right for you.

Design Philosophy
----------------

With the above in mind. The code for this project will follow these goals:

1. Secure defaults - It may be shady, but let's still not get pwned…
2. Dead simple to set up - When using shady, time from project design to
   working product so be as fast as possible.
3. Minimize the amount of JS needed in a project - I hate writing it.

(These are mostly for me to keep in mind while developing.)

What does SHADY-STACK Provide?
------------------------------

You may be asking yourself, what tooling exists for this SHADY-STACK? Well,
while anyone is invited to build on these concepts, the SHADY-STACK repo_ 
provides the following:

- Bridge Applications For:

  - Discord

- A Default API Demon

- Default Hooks For Syncing Via Git

Each of these parts are explained in their respective sections.

Install
-------

The resources provided by the SHADY-STACK repo_ are in the form of a python
model of the name ``shadybackend``.

Currently the default demon and a specified bridge 
can be run as a nix_ flake with:

::

 nix run github:user-1103/shady-stack - <args>
 # To enter a development environment use:
 nix develop github:user-1103/shady-stack

For thoes of you who have yet to see the glory of nix_ the package can be
installed as a poetry_ project.

::

 # Clone the repo.
 git clone https://github.com/user-1103/shady-stack
 # Enter the repo:
 cd shady-stack
 # Install with poetry_
 poetry install
 # Run the backend components
 shadybackend <args>

If you have something against poetry_, you can install the dependencies your
self (found in pyproject.toml). And run:

::

 python3 top_level.py <args>

.. note::
   Need to set up a pip package...

Shady Backend
`````````````
The ``shadybackend`` python module is it the collection of resources provided
by the repo. The Install_ section outlines how to install and run the module
from the command line, subseqently allowing for acess to all the parts provided
by the repo. To progamiticly use the module, see `Progmatic Use`_.

The Default API Demon (DAD)
```````````````````````````
DAD is an extremely bare bones Application Demon. When ``shadybackend`` is run,
it will be started. When run, DAD first looks for user defined APIs to load in
from ``api.py`` in the curent directory.

Defining APIs
-------------

An ``api.py`` file is a normal python file where you can define how your api.

Take the sample below:

..  code-block:: python
    :caption: api.py

    from shadybackend.api_tools import define_api

    @define_api({"example_arg": "default_value", "required_arg_": 1})
    def example_api(G, ARGS):
        ... # Do some api stuff

Lets break down these lines one at a time:

1. Here we import the wraper_ function for defining an api call.

2. A little space to breath.

3. We use the wrapper to define the `baseline arguments`_ for the api.

4. We declare a function that will do the actual backend processing of
   the api. The name of the api call is determined by the name of the function
   and is passed G_, and ARGS_.

Baseline Arguments
~~~~~~~~~~~~~~~~~~

API baselines are one of the defualt security fetures of SHADY-STACK. The
basline for an api exists as a dictionary keyed by strings representing the
name of the argument. The values represent the default values for the argument
if none is provided when the api is called. Before the api funciton is called,
the types of each suplied argument will be compaired to the type of the defualt
value. If they do not match, the api will not be called. If the name of an
arument ends with a ``_``, it will be marked as required. If a required arg is
missing when an api call is requested, the api will not be called. All aruments
provided that are not found in the baseline will be silenty dropped before
being called. Internaly the default JSON_ lib is used and as such, only types
parsed by it can be used in the baseline.

G
~

When an api is called, it has acess to a global dictionary named ``G`` al la flask_.
The data in this variable is shared across all api calls, hooks_, and Application Bridges.

.. note::
   A feature that is being concidered is to save the state of ``G`` across runs of the backend.
   For now though, the state is purged on shutdown.

By default, DAD sets the folowing G_ variables:

+-----------------+--------------------------------------------------+
| Name            | Description                                      | 
+=================+==================================================+
| root            | The path to the location of the local web root.  |
+-----------------+--------------------------------------------------+
| run             | Can be set to false to shutdown the demon.       |
+-----------------+--------------------------------------------------+
| Q               | The queue of Request objects to process.         |
+-----------------+--------------------------------------------------+
| req             | The curent request being processed. Usefull for  |
|                 | error handeling.                                 |
+-----------------+--------------------------------------------------+

`Default bridges`_ may define further values.

.. warning::
   It is probably best to not touch ``Q`` or ``req`` unless you know what you are doing.
   The Requests stored in these variables are not sanitized.

ARGS
~~~~
After the above parsing is done to the aruments provided to the webhook, they
are then provided to the API funciton via the ARGS_ variable.

HOOKS
-----

DAD provides a way to ensure certian actions happen when ceritan events happen
during the execution of DAD. Take the following adition to our ``api.py`` file:

..  code-block:: python
    :caption: api.py

    from shadybackend.api_tools import define_api, define_hook, HookTypes
    import time

    @define_api({"example_arg": "default_value", "required_arg_": 1})
    def example_api(G, ARGS):
        ... # Do some api stuff

    @define_hook(HookTypes.ERR)
    def log_error(G):
        with open("error.log", "a") as f:
            f.write(f"Failed to process request @{time.time()}\n")

This trivial example writes a log file everytime DAD fails to process a
request. The available events you can hook are:

+-----------------+--------------------------------------------------+
| Name            |   Runs On...                                     |
+=================+==================================================+
| HookTypes.ERR   |   ...a failure in processing a request.          |
+-----------------+--------------------------------------------------+
| HookTypes.INIT  |   ...demon startup.                              |
+-----------------+--------------------------------------------------+
| HookTypes.PRE   |   ...the start of processing a request           |
+-----------------+--------------------------------------------------+
| HookTypes.OK    |   ...the successful processing of a request      |
+-----------------+--------------------------------------------------+
| HookTypes.POST  |   ...the end of the processing of a request      |
+-----------------+--------------------------------------------------+
| HookTypes.EXIT  |   ...demon safe exit.                            |
+-----------------+--------------------------------------------------+
| HookTypes.FATAL |   ...demon hitting an unsaveable error.          |
+-----------------+--------------------------------------------------+
| HookTypes.WAIT  |   ...demon idle.                                 |
+-----------------+--------------------------------------------------+

.. hint::
   You can use the ``OK`` hook to sync your local copy of the site to the
   remote static site.


Default Bridges
```````````````

The SHADY-STACK repo_ provides a bunch of defualt bridges that can be activated
with DAD.

Call Structure
--------------

When the user using the static front end of your site needs to do something
dynamic, the JS in the page should call the webhook watched by the Application
Bridge. In this call two things need to be passed the name of the api call to
use, and the aruments to pass to the api call. The bridges defined in the repo
expects the folowing data feilds as a minimum:

+-----------------+--------------------------------------------------+
| Name            | Description                                      | 
+=================+==================================================+
| api_call        | The name of the api to use for the request.      |
+-----------------+--------------------------------------------------+
| data            | A dictionary of args to pass to the request.     |
+-----------------+--------------------------------------------------+

Discord Bridge
-------------

The discord bridge can be used by requesting the ``discord`` from DAD. To use
the bridge you must also set ``discord_token`` to.


Indices and tables
``````````````````

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
