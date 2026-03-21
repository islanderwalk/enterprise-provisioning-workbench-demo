# Interview Story

## Problem

Operators were forced to process repetitive account requests one by one across legacy enterprise admin systems.

## Solution

I designed a desktop batch-processing workspace that:

- extracts inbound requests
- deduplicates conflicting rows
- automates downstream provisioning
- keeps verification and exception handling explicit

The important part is not only automation speed. The real value is reducing operator ambiguity, making external writes deterministic, and keeping enough traceability that a team can audit what happened after a run.

## Engineering Highlights

- deterministic workflow orchestration
- session-aware connector design
- reverse engineering mindset for undocumented or UI-locked workflows
- UI simplification from debug-first to batch-first
- consistent dedupe policy across provisioning and mail delivery
- verification and readback as first-class workflow steps

## How To Talk About It In Interviews

- Start from the operator pain: repeated requests, inconsistent input, and brittle admin systems.
- Explain that the architecture normalizes data before any write, so exceptions are isolated early.
- Describe reverse engineering as workflow analysis, not as a hacking story: page behavior, state transitions, request boundaries, and validation points.
- Emphasize that the goal is safer execution and lower support cost, not flashy automation.
