# Architecture Overview

## Product Goal

Process inbound account requests in batches with minimal operator input and clear final outcomes.

## Core Flow

1. Read source records.
2. Normalize input.
3. Deduplicate by account identity.
4. Decide create, skip, or review.
5. Execute deterministic provisioning steps.
6. Verify results.
7. Produce communication artifacts.

## Showcase Talking Points

- state-machine based automation over legacy admin systems
- batch-level deduplication before external writes
- exception queue instead of step-by-step operator control
- telemetry and replayable execution bundles
