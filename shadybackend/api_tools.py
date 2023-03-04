from dataclasses import dataclass
from enum import auto, Enum
from typing import Any, Callable, Dict, List, Union
from pathlib import Path
import sys
import importlib.util
import logging as log

from shadybackend.request_tools import BadRequest, Request

# The collection of api's
API_GROUP: Dict[str, 'API'] = dict()

# Global api
G: Dict[Any, Any] = dict()

# Keeyed list of hooks to run
HOOKS: Dict['HookTypes', List[Callable]] = dict()


class MalformedAPI(Exception):
    """
    Used when the defined api can not be loaded.
    """
    ...


@dataclass()
class API():
    """
    Represents an api call.
    """
    # The name of the api
    name: str
    # The function to call to execute the api call
    call_function: Callable
    # The basline aruments
    baseline: Dict[str, Any]

    def __call__(self, request: Request) -> None:
        """
        Performs a safe call to the api and logs output.
        """
        safe_data = request.sanitize(self.baseline)
        log = self.call_function(G, safe_data)


def defnine_API(call_function: Callable, baseline: Dict[str, Any]) -> None:
    """
    Warper function to define an api call.
    """
    tmp = API(call_function.__name__, call_function, baseline)
    API_GROUP.update({tmp.name: tmp})
    log.debug(f"Registered {call_function.__name__} with baseline {baseline}")


class HookTypes(Enum):
    """
    The types of hooks that are understood by the system.
    """
    INIT = auto()
    EXIT = auto()
    PRE = auto()
    POST = auto()
    ERR = auto()
    WAIT = auto()
    FATAL = auto()
    OK = auto()


def define_hook(call_function: Callable, hook: HookTypes) -> None:
    """
    Wraper that registers a hook for the given hook type.
    """
    tmp = HOOKS.get(hook, list())
    tmp = [*tmp, call_function]
    HOOKS.update({hook: tmp})
    log.debug(f"Registered {call_function.__name__} for {hook}")


def call_hooks(hook: HookTypes) -> None:
    """
    Calls all hooks registered with a given name.
    """
    h = HOOKS.get(hook, None)
    if ((h is None) or (hook is HookTypes.WAIT)):
        return
    log.debug(f"Calling internal hook {hook}")
    for hook_call in h:
        log.debug(f"Calling {hook_call.__name__}")
        hook_call(G)


def collect_apis(path: Path) -> None:
    """
    Loads the API objects described in the given file.
    """
    try:
        spec = importlib.util.spec_from_file_location("api", path)
        api = importlib.util.module_from_spec(spec)
        sys.modules["api"] = api
        spec.loader.exec_module(api)
        log.info(f"Collected api at {path=}")
    except Exception as e:
        raise MalformedAPI(f"Could not load API: \n {e}")


def process_request(request: Request) -> None:
    """
    Takes a request, finds the necessary api and process the given data with said api.
    """
    api = API_GROUP.get(request.api_call, None)
    if (api is None):
        raise BadRequest(f"Unknown API '{request.api_call}'")
    else:
        log.debug(f"Processing {request} with {api}")
        api(request)
