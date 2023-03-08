# SHADY Stack

As the name implies, this is a less than kosher web stack. I developed it for
my projects as I am in university and web hosting can be expensive. The shady stack consists of the following:

1. A **S**tatic site hosted (GitHub Pages, GitLab Pages, ECT.)
2. Simplistic pages that communicate to the backend via a already existing web-app's Web **H**ooks (Slack, Discord, Gsuit, GitHub Actions, ECT.).
3. An **A**plication Bridge program that can read the calls to the webhooks and pass them to the next component.
4. A Backend **D**eamon that acutely presses the requests from the webhooks and updates a local copy of the site tree as needed.
5. An application that regularly s**Y**ncs the local tree with the remote tree served as the static site in step 1.

## Pros And Cons

There are some ups and downs to using this stack.

| Pros | Cons |
|------|------|
| Backend is hidden behind a proxy of sorts. | Failure or delay in the web hook provider means failure / delay in your site. |
| It's free! | Depending on the web hook provider, it may be breaking a TOS or two |
| It's kinda fail-safe. If the backend breaks, the static parts of your site will still work | The number of components between your frontend and backend means it's slow to update. |

## Design Goals

With the above in mind. The code for this project will follow these goals:

1. Secure defaults - It may be shady, but let's still not get pwned…
2. Dead simple to set up - When using shady, time from project design to working product so be as fast as possible.
3. Minimize the amount of JS needed in a project - I hate writing it.

(These are mostly for me to keep in mind while developing).

## System Design

The stack has three things that are not already implemented by other applications. This repo fills in the holes.

### Application Bridge(s)

The bridge submodule of this package provides a collection of application bridges, all of which do the following:

- Attach to the applicable web hook provider.
- Read any incoming webhooks.
- Write the request to a [Unix Named Pipe](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjb0cPk1Kz9AhXmAzQIHcQRD6IQFnoECAwQAQ&url=https%3A%2F%2Fman7.org%2Flinux%2Fman-pages%2Fman7%2Ffifo.7.html&usg=AOvVaw2_M936WOCsiGhCs-OLBNZT).


### Backend Demon

This repo provides one demon for backend processing (known as the Default Demon
(DD)). The DD is given a directory that looks like the following:

```
- ./request.fifo
- ./api.py
- ./tree
  - index.html
  - <other web files> 
```

Where `api.py` is a file that contains functions of the form:

```python3

def api_call_name(tree: Tree, request: Dict[str, Any]) -> Tree:
    """
    This is a function that represents an action your front end can request of your backend.

    :args tree: Tree object (see documentation) that represents the state of the site file tree (./tree).
    :args request: A JSON to Dict representation of the original request to the api.
    :return: The original tree parameter, now modified, and passed back.
    """

    # Do stuff to modify the site in accordance to the request.

    return tree
```

`request.fifo` is a Unix Named Pipe that the Application Bridge writes to. `tree` is the local copy of the site tree.

### Sync Application

The sync application is a very simple program that runs on occasion and checks
the local tree and if any changes have been made, they are pushed to the static
site host. Currently, the only sync application that is currently provided by this
repo is for git.

### Request Structure

In adtion to the above code, this repo defines the format for a SHADY web-hook request. 
