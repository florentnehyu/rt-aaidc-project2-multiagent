# src/state.py
from typing import Any, Dict

class MASState:
    """
    Simple shared state for multi-agent system.
    Stores intermediate outputs under named keys.
    """
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def to_dict(self):
        return dict(self.data)