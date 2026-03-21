# Enterprise Provisioning Workbench Demo

Sanitized public showcase for a desktop automation workspace that converts repetitive account requests into a deterministic batch workflow.

This repository is the public-safe derivative of a private internal project. It focuses on architecture, workflow design, and safe abstractions without exposing production connectors, internal targets, or sensitive runtime data.

It is positioned for portfolio review, technical interviews, and resume links where the reader needs to understand both the engineering rigor and the operational pain it solves.

## Execution Evidence

The screenshot below is generated from a real local run of the sanitized demo workflow, not from a mock UI.

![Sanitized demo run summary](docs/screenshots/run-summary.svg)

What this proves:

- the public repo can be executed end-to-end with sample data
- normalization, merge policy, and action planning are visible in one run
- the `create / review / skip` split is backed by an actual report, not only architecture notes

## Positioning

This workbench is a desktop-oriented operator workspace, not a generic AI agent framework.

The product goal is to move operators away from one-by-one request handling and toward:

- batch intake from inbound request sources
- normalized request rows before downstream execution
- deduplication and merge policy before any external write
- explicit `create`, `skip`, or `review` outcomes
- communication artifacts generated from verified results

## High-Level Architecture

```mermaid
flowchart TB
    Operator["Operator Workspace<br>Launcher / Status / Run Summary"]
    Inbox["Inbound Requests<br>Email / File / Queue"]

    subgraph Engine["Batch Decision Engine"]
        Normalize["Normalize Rows"]
        Merge["Deduplicate and Merge"]
        Plan["Plan Create / Skip / Review"]
    end

    subgraph Adapters["Deterministic Adapters"]
        Provision["Provisioning Connector"]
        Notify["Draft Generator"]
    end

    subgraph Outputs["Operator Artifacts"]
        Summary["Execution Summary"]
        Review["Review Queue"]
        Drafts["Draft Previews"]
    end

    Inbox --> Operator
    Operator --> Normalize
    Normalize --> Merge
    Merge --> Plan
    Plan --> Provision
    Plan --> Notify
    Plan --> Review
    Provision --> Summary
    Notify --> Drafts

    classDef shell fill:#f6f0e7,stroke:#7b5a2e,color:#2f2417;
    classDef engine fill:#e9f1ea,stroke:#4b6a50,color:#1d2b1f;
    classDef adapter fill:#e8eef7,stroke:#40618a,color:#13263f;
    classDef output fill:#f4e8ed,stroke:#8a4d63,color:#351620;

    class Operator,Inbox shell;
    class Normalize,Merge,Plan engine;
    class Provision,Notify adapter;
    class Summary,Review,Drafts output;
```

### Workspace shell

- launcher-driven tool surfaces
- shared execution entry points
- operator-facing status, logs, and result summaries

### Batch processing layer

- source record ingestion
- row normalization
- deduplication and merge policy
- exception-focused review queues

### Deterministic adapters

- provisioning connectors perform controlled external writes
- notification adapters render communication artifacts
- AI may assist extraction or interpretation, but not final system writes

### Observability

- execution summaries
- replay-friendly telemetry events
- debug bundles kept only in private environments

## Core Operator Flow

1. Read inbound request records.
2. Normalize the input into consistent account rows.
3. Merge duplicates before any downstream write.
4. Decide whether each account should be created, skipped, or reviewed.
5. Execute deterministic provisioning steps.
6. Verify the result.
7. Generate outbound draft communication for valid outcomes.

## Product Design Principles

- batch-first UX
- one primary operator action for the happy path
- exceptions expanded only when needed
- deterministic adapters own external writes
- public documentation stays high-level and sanitized

## Why This Plays Well On A Resume

- shows batch-first workflow design instead of one-off scripting
- demonstrates reverse engineering mindset without exposing private browser traces
- frames automation as a controls and auditability problem, not just a convenience script
- gives interviewers a clean story around normalization, deduplication, verification, and operator safety

## Interview Materials

- `docs/interview-story.md`: concise narrative for interview answers
- `docs/architecture-overview.md`: technical walk-through for system design conversations
- `docs/104-link-copy.md`: ready-to-paste title and description for 104 or similar profile links
- `docs/sanitization-checklist.md`: boundary checklist for public-safe releases

## Demo App

`demo_app/` is a sanitized Python reference implementation of the architecture above. It demonstrates:

- request normalization
- duplicate merging by account identity
- deterministic action planning
- fake provisioning execution
- draft preview generation

Run the demo as a portfolio-style CLI:

```bash
python -m demo_app --show-stages
```

Export sample input and run from a JSON file:

```bash
python -m demo_app sample --output sample-output/requests.json
python -m demo_app --input sample-output/requests.json --save-report sample-output/run-report.json
```

Run the tests:

```bash
python -m unittest discover -s tests
```

## Repository Layout

- `demo_app/`: sanitized Python workflow skeleton
- `docs/architecture-overview.md`: high-level architecture summary
- `docs/interview-story.md`: portfolio framing and interview narrative
- `docs/sanitization-checklist.md`: public release boundary checklist
- `tests/`: public-safe tests for the demo workflow

## CLI Preview

```text
ENTERPRISE PROVISIONING WORKBENCH DEMO
=======================================
Source: sample-data
Ingested requests: 4
Unique accounts:   3
Decision mix:     create=1  review=1  skip=1

ACTION BOARD
------------
+--------------------+----------+------------+------------------------------------------------------+
| Account            | Decision | Access     | Reason                                               |
+--------------------+----------+------------+------------------------------------------------------+
| alice.chen         | CREATE   | MAIL, VPN  | Safe deterministic batch create.                     |
| carol.lin          | REVIEW   | ADMIN      | High-impact access or complex merge requires oper... |
| existing-bob.wu    | SKIP     | VPN        | Existing account detected by deterministic lookup... |
+--------------------+----------+------------+------------------------------------------------------+
```

## Public Safety Boundary

This repository intentionally excludes:

- internal company systems and URLs
- real credentials, cookies, and tokens
- real customer or account data
- raw HTML captures and reverse-engineering traces
- production debug bundles and telemetry payloads

## License

MIT. See `LICENSE`.
