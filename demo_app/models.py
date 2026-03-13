from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class RawRequest:
    request_id: str
    account_key: str
    display_name: str
    requested_access: str
    source_channel: str = "email"


@dataclass(frozen=True)
class NormalizedRequest:
    request_id: str
    account_key: str
    display_name: str
    requested_access: str
    source_channel: str


@dataclass(frozen=True)
class WorkItem:
    account_key: str
    display_name: str
    requested_access: tuple[str, ...]
    source_channels: tuple[str, ...]
    merged_request_ids: tuple[str, ...]


class Action(str, Enum):
    CREATE = "create"
    SKIP = "skip"
    REVIEW = "review"


@dataclass(frozen=True)
class PlannedAction:
    account_key: str
    display_name: str
    action: Action
    reason: str
    requested_access: tuple[str, ...]
    merged_request_ids: tuple[str, ...]


@dataclass(frozen=True)
class BatchRunSummary:
    ingested_count: int
    unique_accounts: int
    actions: tuple[PlannedAction, ...]
    provisioning_events: tuple[str, ...]
    draft_previews: tuple[str, ...]
