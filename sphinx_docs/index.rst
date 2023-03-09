.. SHADY-STACK documentation master file, created by
   sphinx-quickstart on Tue Mar  7 16:35:16 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _repo: https://github.com/user-1103/shady-stack

Welcome to SHADY-STACK
======================

What Is SHADY-STACK?
```````````````````

As the name implies, this is a less than kosher web stack based of of the SWAG
stack. I developed it for my projects as I am in university and web hosting can
be expensive. The shady stack consists of the following:  

1. A **S** tatic site hosted (GitHub Pages, GitLab Pages, ECT.) 
2. Simplistic pages that communicate to the backend via a already existing web-app's Web
   **H** ooks (Slack, Discord, Gsuit, GitHub Actions, ECT.).  
3. An **A** plication Bridge program that can read the calls to the webhooks and
   pass them to the next component. 
4. A Backend **D** eamon that acutely presses the requests from the webhooks and
   updates a local copy of the site tree as needed.  
5. An application that regularly s **Y** ncs the local tree
   with the remote tree served as the static site in step 1.


What Is This?
`````````````

In this webpage you will find the documentation for using the SHADY-STACK.

.. note::

    This sample documentation was generated on |today|, and is rebuilt with
    each release.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Overview
________

Before we dive into the stack, lets talk about the abstract concepts.

Is SHADY-STACK Right For You?
`````````````````````````````
There are some ups and downs to using this stack.

+--------------------------------+----------------------------------+
| Pros                           | Cons                             |
+================================+==================================+
| Backend is hidden behind a     | Failure or delay in the web hook |
| proxy of sorts.                | provider means failure / delay   |
|                                | in your site.                    |
+--------------------------------+----------------------------------+
| It's free!                     | Depending on the web hook        |
|                                | provider, it may be breaking a   |
|                                | TOS or two                       |
+--------------------------------+----------------------------------+
| It's kinda fail-safe.          | The number of components between |
| If the backend breaks,         | your frontend and backend means  |
| the static parts of your       | it's slow to update.             |
| site will still work           |                                  |
+--------------------------------+----------------------------------+

Remember to consult your physician to see if SHADY-STACK is right for you.

Design Philosophy
````````````````

With the above in mind. The code for this project will follow these goals:

1. Secure defaults - It may be shady, but let's still not get pwned…
2. Dead simple to set up - When using shady, time from project design to
   working product so be as fast as possible.
3. Minimize the amount of JS needed in a project - I hate writing it.

(These are mostly for me to keep in mind while developing).

What does SHADY-STACK Provide?
``````````````````````````````
You may be asking yourself, what tooling exists for this SHADY-STACK? Well,
while anyone is invited to build on these concepts, the SHADY-STACK repo_ 
provides the following:

- Bridge Applications For:
  - Discord
- A Default API Demon
- Default Hooks For Syncing Via Git

Each of these parts are explained in their respective sections.

Install
```````




Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
