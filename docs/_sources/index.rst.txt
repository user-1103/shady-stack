.. SHADY-STACK documentation master file, created by
   sphinx-quickstart on Tue Mar  7 16:35:16 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

In this webpage you will find the document for using the SHADY-STACK.

.. note::

    This sample documentation was generated on |today|, and is rebuilt weekly.


Table Of Contents
`````````````````
.. toctree::
   :maxdepth: 2
   :caption: Contents:


Overview
________

Before we dive into the stack, lets talk about the abstract concepts.

Is SHADY-STACK Right For You?
`````````````````````````````
There are some ups and downs to using this stack.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
