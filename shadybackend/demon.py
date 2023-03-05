"""
This is the default API demon that is used for the shadybackend.
"""
from pathlib import Path
from typing import List
from shadybackend.api_tools import G, HOOKS, HookTypes, call_hooks, process_request, collect_apis
from collections import deque
from time import sleep
import logging as log

G["Q"] = deque()

MAX_SLEEP = 1


def run_api_demon(root: Path, api_paths: List[Path]) -> None:
    """
    Run the app, with self restarting on recoverable errors.
    """
    G["root"] = root
    G["run"] = True
    call_hooks(HookTypes.INIT)
    for path in api_paths:
        collect_apis(path)
    try:
        while (G["run"]):
            if (len(G["Q"])):
                call_hooks(HookTypes.PRE)
                req = G["Q"].pop()
                try:
                    process_request(req)
                except Exception as e:
                    call_hooks(HookTypes.ERR)
                    err = e
                    log.error(f"Failed to process {req}: {e}")
                else:
                    call_hooks(HookTypes.OK)
                finally:
                    call_hooks(HookTypes.POST)
            else:
                call_hooks(HookTypes.WAIT)
                sleep(MAX_SLEEP)
        call_hooks(HookTypes.EXIT)
    except Exception as e:
        log.fatal(f"Fatal err: {e}")
        call_hooks(HookTypes.FATAL)


log.debug("Loaded demon lib.")
