from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .adapters import DraftPreviewAdapter, InMemorySourceAdapter, SimulatedProvisioningAdapter
from .models import BatchRunSummary, RawRequest
from .pipeline import run_demo
from .sample_data import SAMPLE_EXISTING_ACCOUNTS, SAMPLE_REQUESTS


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the sanitized provisioning workflow demo.")
    parser.add_argument("--input", type=Path, help="JSON input file; defaults to bundled sample data.")
    parser.add_argument("--save-report", type=Path, help="Write the JSON run report to this path.")
    parser.add_argument("--show-stages", action="store_true", help="Print a compact operator-oriented summary.")
    subparsers = parser.add_subparsers(dest="command")
    sample = subparsers.add_parser("sample", help="Write a valid sample input file.")
    sample.add_argument("--output", type=Path, required=True)
    return parser


def _sample_payload() -> dict[str, Any]:
    return {
        "requests": [asdict(item) for item in SAMPLE_REQUESTS],
        "existing_accounts": sorted(SAMPLE_EXISTING_ACCOUNTS),
    }


def _load_payload(path: Path | None) -> tuple[list[RawRequest], set[str]]:
    if path is None:
        return list(SAMPLE_REQUESTS), set(SAMPLE_EXISTING_ACCOUNTS)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("requests"), list):
        raise ValueError("Input must be an object containing a 'requests' array.")
    requests = [RawRequest(**item) for item in payload["requests"]]
    existing = {str(item).strip().casefold() for item in payload.get("existing_accounts", []) if str(item).strip()}
    return requests, existing


def _report_payload(summary: BatchRunSummary) -> dict[str, Any]:
    return asdict(summary)


def _print_stages(summary: BatchRunSummary) -> None:
    counts = {action: 0 for action in ("create", "review", "skip")}
    for item in summary.actions:
        counts[item.action.value] += 1
    print("ENTERPRISE PROVISIONING WORKBENCH DEMO")
    print(f"Ingested requests: {summary.ingested_count}")
    print(f"Unique accounts:   {summary.unique_accounts}")
    print(f"Decision mix:      create={counts['create']} review={counts['review']} skip={counts['skip']}")
    print("\nACTION BOARD")
    for item in summary.actions:
        access = ",".join(item.requested_access)
        print(f"- {item.account_key:20} {item.action.value.upper():6} {access:12} {item.reason}")


def main() -> None:
    args = _parser().parse_args()
    if args.command == "sample":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(_sample_payload(), indent=2), encoding="utf-8")
        print(args.output)
        return

    requests, existing_accounts = _load_payload(args.input)
    summary = run_demo(
        source=InMemorySourceAdapter(requests),
        provisioning=SimulatedProvisioningAdapter(existing_accounts),
        notifications=DraftPreviewAdapter(),
    )
    payload = _report_payload(summary)
    if args.save_report:
        args.save_report.parent.mkdir(parents=True, exist_ok=True)
        args.save_report.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.show_stages:
        _print_stages(summary)
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
