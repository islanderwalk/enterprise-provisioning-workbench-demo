# Interview Story

## Problem

Operators were forced to process repetitive account requests one by one across legacy enterprise admin systems.

## Solution

I designed a desktop batch-processing workspace that:

- extracts inbound requests
- deduplicates conflicting rows
- automates downstream provisioning
- keeps verification and exception handling explicit

## Engineering Highlights

- deterministic workflow orchestration
- session-aware connector design
- UI simplification from debug-first to batch-first
- consistent dedupe policy across provisioning and mail delivery
