"""
A central module to look up the available backends.
"""

from dataclasses import dataclass
from typing import Callable, Dict

BRIDGES: Dict[str, 'Bridge'] = dict()


@dataclass
class Bridge():
    """
    Generic form of a bridge to be subclassed.
    """
    # The name of the bridge, used for lookup
    name: str
    # method that runs the bridge
    build_bridge: Callable

    def __post_init__(self) -> None:
        """
        Adds the bridge to the global dict.
        """
        BRIDGES.update({self.name: self})
