# Architecture Overview

## Positioning

The workbench is a desktop-oriented internal automation workspace designed for batch operations, not one-off manual handling.

Its role is to turn repetitive inbound account requests into a deterministic workflow with explicit outcomes and clear auditability.

## Core Flow

1. Read source records from an inbound channel.
2. Normalize them into a stable request shape.
3. Merge duplicate rows before any external write.
4. Decide `create`, `skip`, or `review`.
5. Execute deterministic provisioning steps.
6. Verify results and capture a summary.
7. Produce communication artifacts for valid outcomes.

## Major Subsystems

### Workspace shell

- tool launcher
- operator status and logs
- shared execution entry point

### Batch processing layer

- normalization
- deduplication
- merge policy
- exception queue

### Deterministic adapters

- provisioning connectors
- notification rendering
- safe execution boundaries

### Observability

- execution summaries
- telemetry events
- replay-friendly debug artifacts in private environments only

## Showcase Talking Points

- batch-first UX over step-by-step operator control
- state-machine oriented automation for brittle admin systems
- deduplication before external writes
- deterministic adapters instead of direct UI logic
