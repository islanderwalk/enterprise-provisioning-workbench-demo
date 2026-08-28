from __future__ import annotations

import unittest

from demo_app.adapters import DraftPreviewAdapter, InMemorySourceAdapter, SimulatedProvisioningAdapter
from demo_app.models import Action, RawRequest
from demo_app.pipeline import merge_requests, normalize_requests, plan_actions, run_demo


class PipelineTests(unittest.TestCase):
    def test_merge_requests_deduplicates_by_normalized_account_key(self) -> None:
        raw_requests = [
            RawRequest("REQ-1", "alice", "Alice", "vpn"),
            RawRequest("REQ-2", " ALICE ", "Alice", "mail"),
        ]
        merged = merge_requests(normalize_requests(raw_requests))
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].requested_access, ("MAIL", "VPN"))

    def test_normalize_requests_rejects_missing_required_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "account_key"):
            normalize_requests([RawRequest("REQ-1", " ", "Alice", "vpn")])

    def test_plan_actions_uses_adapter_readback_for_existing_accounts(self) -> None:
        items = merge_requests(normalize_requests([RawRequest("REQ-1", "alice", "Alice", "vpn")]))
        actions = plan_actions(items, lambda account_key: account_key == "alice")
        self.assertEqual(actions[0].action, Action.SKIP)

    def test_plan_actions_routes_admin_access_to_review(self) -> None:
        items = merge_requests(normalize_requests([RawRequest("REQ-1", "alice", "Alice", "admin")]))
        actions = plan_actions(items, lambda _: False)
        self.assertEqual(actions[0].action, Action.REVIEW)

    def test_run_demo_generates_events_and_drafts_for_create_only(self) -> None:
        raw_requests = [
            RawRequest("REQ-1", "alice", "Alice", "vpn"),
            RawRequest("REQ-2", "bob", "Bob", "vpn"),
            RawRequest("REQ-3", "carol", "Carol", "admin"),
        ]
        summary = run_demo(
            source=InMemorySourceAdapter(raw_requests),
            provisioning=SimulatedProvisioningAdapter({"bob"}),
            notifications=DraftPreviewAdapter(),
        )
        self.assertEqual([item.action for item in summary.actions], [Action.CREATE, Action.SKIP, Action.REVIEW])
        self.assertEqual(len(summary.provisioning_events), 1)
        self.assertEqual(len(summary.draft_previews), 1)


if __name__ == "__main__":
    unittest.main()
