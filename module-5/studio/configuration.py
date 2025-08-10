import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated
from dataclasses import dataclass

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the chatbot."""
    user_id: str = "default-user"

    def __init__(self, user_id: str = "default-user", **kwargs: Any):
        self.user_id = user_id
        # Store any extra keys without error
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        configurable = (config.get("configurable", {}) if config else {})
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls) if f.init
        }
        # Merge known + unknown keys
        merged = {**configurable, **{k: v for k, v in values.items() if v is not None}}
        return cls(**merged)
