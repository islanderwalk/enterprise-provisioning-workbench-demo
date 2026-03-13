from __future__ import annotations

from .adapters import NotificationAdapter, ProvisioningAdapter, SourceAdapter
from .models import Action, BatchRunSummary, NormalizedRequest, PlannedAction, RawRequest, WorkItem


def normalize_requests(raw_requests: list[RawRequest]) -> list[NormalizedRequest]:
    return [
        NormalizedRequest(
            request_id=item.request_id.strip(),
            account_key=item.account_key.strip().lower(),
            display_name=" ".join(item.display_name.split()),
            requested_access=item.requested_access.strip().upper(),
            source_channel=item.source_channel.strip().lower(),
        )
        for item in raw_requests
    ]


def merge_requests(normalized_requests: list[NormalizedRequest]) -> list[WorkItem]:
    grouped: dict[str, dict[str, object]] = {}
    for item in normalized_requests:
        bucket = grouped.setdefault(
            item.account_key,
            {
                "display_name": item.display_name,
                "requested_access": set(),
                "source_channels": set(),
                "merged_request_ids": [],
            },
        )
        bucket["requested_access"].add(item.requested_access)
        bucket["source_channels"].add(item.source_channel)
        bucket["merged_request_ids"].append(item.request_id)

    work_items: list[WorkItem] = []
    for account_key, bucket in grouped.items():
        work_items.append(
            WorkItem(
                account_key=account_key,
                display_name=str(bucket["display_name"]),
                requested_access=tuple(sorted(bucket["requested_access"])),
                source_channels=tuple(sorted(bucket["source_channels"])),
                merged_request_ids=tuple(bucket["merged_request_ids"]),
            )
        )
    return sorted(work_items, key=lambda item: item.account_key)


def plan_actions(work_items: list[WorkItem]) -> list[PlannedAction]:
    planned: list[PlannedAction] = []
    for item in work_items:
        if item.account_key.startswith("existing-"):
            action = Action.SKIP
            reason = "Existing account detected by deterministic lookup rule."
        elif "ADMIN" in item.requested_access or len(item.requested_access) > 2:
            action = Action.REVIEW
            reason = "High-impact access or complex merge requires operator review."
        else:
            action = Action.CREATE
            reason = "Safe deterministic batch create."

        planned.append(
            PlannedAction(
                account_key=item.account_key,
                display_name=item.display_name,
                action=action,
                reason=reason,
                requested_access=item.requested_access,
                merged_request_ids=item.merged_request_ids,
            )
        )
    return planned


def run_demo(
    source: SourceAdapter,
    provisioning: ProvisioningAdapter,
    notifications: NotificationAdapter,
) -> BatchRunSummary:
    raw_requests = source.fetch_requests()
    normalized_requests = normalize_requests(raw_requests)
    work_items = merge_requests(normalized_requests)
    actions = plan_actions(work_items)
    provisioning_events = provisioning.apply(actions)
    draft_previews = notifications.build_drafts(actions)
    return BatchRunSummary(
        ingested_count=len(raw_requests),
        unique_accounts=len(work_items),
        actions=tuple(actions),
        provisioning_events=provisioning_events,
        draft_previews=draft_previews,
    )
