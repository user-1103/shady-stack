from pathlib import Path
from typing import List
from util.api_tools import G, HOOKS, HookTypes, call_hooks, process_request, collect_apis
from collections import deque
from time import sleep

G["Q"] = deque()

MAX_SLEEP = 1


def run_api_demon(root: Path, api_paths: List[Path]) -> None:
    """
    Run the app, with self restarting on recoverable errors.
    """
    G["root"] = root
    call_hooks(HookTypes.INIT)
    for path in api_paths:
        collect_apis(path)
    while True:
        if (len(G["Q"])):
            call_hooks(HookTypes.PRE)
            req = G["Q"].pop()
            try:
                process_request(req)
            except Exception as e:
                call_hooks(HookTypes.ERR)
                err = e
            else:
                call_hooks(HookTypes.OK)
            finally:
                call_hooks(HookTypes.FATAL)
            call_hooks(HookTypes.POST)
        else:
            call_hooks(HookTypes.EXIT)
            sleep(MAX_SLEEP)
