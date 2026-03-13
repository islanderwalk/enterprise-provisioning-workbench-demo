from __future__ import annotations

import unittest

from demo_app.adapters import DraftPreviewAdapter, InMemorySourceAdapter, SimulatedProvisioningAdapter
from demo_app.models import Action, RawRequest
from demo_app.pipeline import merge_requests, normalize_requests, plan_actions, run_demo


class PipelineTests(unittest.TestCase):
    def test_merge_requests_deduplicates_by_account_key(self) -> None:
        raw_requests = [
            RawRequest("REQ-1", "alice", "Alice", "vpn"),
            RawRequest("REQ-2", " ALICE ", "Alice", "mail"),
        ]

        normalized = normalize_requests(raw_requests)
        merged = merge_requests(normalized)

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].requested_access, ("MAIL", "VPN"))

    def test_plan_actions_skips_existing_accounts(self) -> None:
        raw_requests = [RawRequest("REQ-1", "existing-alice", "Alice", "vpn")]

        actions = plan_actions(merge_requests(normalize_requests(raw_requests)))

        self.assertEqual(actions[0].action, Action.SKIP)

    def test_run_demo_generates_drafts_for_create_only(self) -> None:
        raw_requests = [
            RawRequest("REQ-1", "alice", "Alice", "vpn"),
            RawRequest("REQ-2", "existing-bob", "Bob", "vpn"),
            RawRequest("REQ-3", "carol", "Carol", "admin"),
        ]

        summary = run_demo(
            source=InMemorySourceAdapter(raw_requests),
            provisioning=SimulatedProvisioningAdapter(),
            notifications=DraftPreviewAdapter(),
        )

        self.assertEqual(summary.unique_accounts, 3)
        self.assertEqual(len(summary.provisioning_events), 1)
        self.assertEqual(len(summary.draft_previews), 1)


if __name__ == "__main__":
    unittest.main()
