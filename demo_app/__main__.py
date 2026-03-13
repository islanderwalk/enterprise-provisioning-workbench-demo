from __future__ import annotations

import json
from dataclasses import asdict

from .adapters import DraftPreviewAdapter, InMemorySourceAdapter, SimulatedProvisioningAdapter
from .pipeline import run_demo
from .sample_data import SAMPLE_REQUESTS


def main() -> None:
    summary = run_demo(
        source=InMemorySourceAdapter(SAMPLE_REQUESTS),
        provisioning=SimulatedProvisioningAdapter(),
        notifications=DraftPreviewAdapter(),
    )
    print(json.dumps(asdict(summary), indent=2))


if __name__ == "__main__":
    main()
