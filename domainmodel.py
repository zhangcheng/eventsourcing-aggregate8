from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel

from eventsourcing.domain import (
    Aggregate as BaseAggregate,
    CanInitAggregate,
    CanMutateAggregate,
    CanSnapshotAggregate,
    event,
)


class DomainEvent(BaseModel):
    originator_id: UUID
    originator_version: int
    timestamp: datetime

    class Config:
        allow_mutation = False


class Aggregate(BaseAggregate):
    class Event(DomainEvent, CanMutateAggregate):
        pass

    class Created(Event, CanInitAggregate):
        originator_topic: str


class Snapshot(DomainEvent, CanSnapshotAggregate):
    topic: str
    state: Dict[str, Any]


@dataclass
class Trick():
    name: str


class Dog(Aggregate):
    @event("Registered")
    def __init__(self, name: str) -> None:
        self.name = name
        self.tricks: List[Trick] = []

    @event("TrickAdded")
    def add_trick(self, trick: str) -> None:
        self.tricks.append(Trick(name=trick))
