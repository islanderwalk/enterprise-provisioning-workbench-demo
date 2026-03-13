from __future__ import annotations

from .models import RawRequest

SAMPLE_REQUESTS = [
    RawRequest(
        request_id="REQ-1001",
        account_key="alice.chen",
        display_name="Alice Chen",
        requested_access="vpn",
    ),
    RawRequest(
        request_id="REQ-1002",
        account_key=" alice.chen ",
        display_name="Alice   Chen",
        requested_access="mail",
    ),
    RawRequest(
        request_id="REQ-1003",
        account_key="existing-bob.wu",
        display_name="Bob Wu",
        requested_access="vpn",
    ),
    RawRequest(
        request_id="REQ-1004",
        account_key="carol.lin",
        display_name="Carol Lin",
        requested_access="admin",
    ),
]
