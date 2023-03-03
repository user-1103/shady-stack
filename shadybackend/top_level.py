import logging as log
log.basicConfig(level=log.DEBUG)
from pathlib import Path
from typing import Dict, Any
from threading import Thread
from sys import exit
from signal import signal, SIGINT

from shadybackend.discord_bridge import build_bridge
from shadybackend.api_tools import G, HookTypes, call_hooks
from shadybackend.demon import run_api_demon

DEFAULT_WEB_ROOT = "./tree"
DEFAULT_API_ROOT = "./api.py"

def run_top_level(start_g: Dict[str, Any], bridge: str,
                  root: str = DEFAULT_WEB_ROOT, api: str = DEFAULT_API_ROOT) -> None:
    """
    Starts the provided hook bridge and runs the default demon.
    """
    root_path = Path(root)
    api_path = [Path(api)]
    log.debug(f"Using {root_path=} {api_path=}")
    G.update(start_g)
    log.debug(f"Using {start_g=}")
    api_thread = Thread(target=run_api_demon, name="API Demon",
                        args=[root_path, api_path], daemon=True)
    bridge_thread = Thread(target=build_bridge, name="Hook Bridge",
                           args=[G], daemon=True)
    log.info("Starting API Demon thread")
    api_thread.start()
    log.info("Starting API Bridge thread")
    bridge_thread.start()
    while True:
        ...

def on_exit(signum, stack) -> None:
    """
    Calls the redigested EXIT hooks on kill signal
    """
    log.fatal("Killed by user")
    call_hooks(HookTypes.EXIT)
    exit(0)

signal(SIGINT, on_exit)

def run() -> None:
    with open("keys") as f:
        token = f.readline()[:-1]
    run_top_level({"discord_token": token}, "fish")

if __name__ == "__main__":
    run()
