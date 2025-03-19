from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class BaseMessage(ABC):
    """Base class for all messages exchanged."""

    version: str = "0.0.1"
    """The version of the format."""

    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(encoder=datetime.isoformat, decoder=datetime.fromisoformat),
    )
    """The timestamp of the message."""

    text: str
    """The text of the message."""


@dataclass_json
@dataclass(kw_only=True)
class TextMessage(BaseMessage):
    """A message containing text and speaker."""

    speaker: str
    """Identifier of the author of the message."""


@dataclass_json
@dataclass(kw_only=True)
class ObservationMessage(BaseMessage):
    """A message containing an observation."""
    pass
