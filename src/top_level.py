from pathlib import Path
from typing import Dict, Any
from threading import Thread
from bridge.discord_bridge import build_bridge
from util.api_tools import G
from default_demon.demon import run_api_demon

DEFAULT_WEB_ROOT = "./tree"
DEFAULT_API_ROOT = "./api.py"

def run_top_level(start_g: Dict[str, Any], bridge: str,
                  root: str = DEFAULT_WEB_ROOT, api: str = DEFAULT_API_ROOT) -> None:
    """
    Starts the provided hook bridge and runs the default demon.
    """
    root_path = Path(root)
    api_path = [Path(api)]
    G.update(start_g)
    api_thread = Thread(target=run_api_demon, name="API Demon",
                        args=[root_path, api_path], daemon=True)
    bridge_thread = Thread(target=build_bridge, name="Hook Bridge",
                           args=[G], daemon=True)
    api_thread.run()
    bridge_thread.run()


