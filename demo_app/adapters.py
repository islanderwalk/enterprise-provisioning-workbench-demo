from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence

from .models import Action, PlannedAction, RawRequest


class SourceAdapter(Protocol):
    def fetch_requests(self) -> list[RawRequest]:
        ...


class ProvisioningAdapter(Protocol):
    def apply(self, actions: Sequence[PlannedAction]) -> tuple[str, ...]:
        ...


class NotificationAdapter(Protocol):
    def build_drafts(self, actions: Sequence[PlannedAction]) -> tuple[str, ...]:
        ...


@dataclass
class InMemorySourceAdapter:
    requests: list[RawRequest]

    def fetch_requests(self) -> list[RawRequest]:
        return list(self.requests)


class SimulatedProvisioningAdapter:
    def apply(self, actions: Sequence[PlannedAction]) -> tuple[str, ...]:
        events: list[str] = []
        for action in actions:
            if action.action is Action.CREATE:
                access = ", ".join(action.requested_access)
                events.append(f"SIMULATED CREATE {action.account_key} [{access}]")
        return tuple(events)


class DraftPreviewAdapter:
    def build_drafts(self, actions: Sequence[PlannedAction]) -> tuple[str, ...]:
        drafts: list[str] = []
        for action in actions:
            if action.action is Action.CREATE:
                access = ", ".join(action.requested_access)
                drafts.append(f"Draft for {action.display_name} <{action.account_key}>: {access}")
        return tuple(drafts)
