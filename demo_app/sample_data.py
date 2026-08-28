from __future__ import annotations

from .models import RawRequest

SAMPLE_REQUESTS = [
    RawRequest("REQ-1001", "alice.chen", "Alice Chen", "vpn"),
    RawRequest("REQ-1002", " alice.chen ", "Alice   Chen", "mail"),
    RawRequest("REQ-1003", "bob.wu", "Bob Wu", "vpn"),
    RawRequest("REQ-1004", "carol.lin", "Carol Lin", "admin"),
]

SAMPLE_EXISTING_ACCOUNTS = {"bob.wu"}
