---
title: Manifesto
purpose: Manifesto of the CVLN Intelligence OS specification.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Manifesto

## Specification is separate from implementation

CVLN's architecture is written down so that it can be argued with. A repository that
cannot be contradicted by evidence is marketing.

## Evidence precedes architecture

The sequence is fixed: evidence → reconstruction → model → specification → gaps →
proposals. The inverse sequence — assumption → architecture → asserted capability —
is prohibited.

## Four levels, never conflated

`CONCEPT`, `SPECIFICATION`, `IMPLEMENTATION`, `DEPLOYED RUNTIME`. A specification is
not a capability. A filename is not a subsystem. A README is not a runtime.

## Absence is reported

Where evidence is missing, the required statement is
**NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES** — not a plausible guess. The
audited estate already practises this: META's loop maps return
`DATA_NOT_AVAILABLE` rather than inventing a number. That standard is inherited here.

## Nothing invented is presented as existing

ISA and MCL are proposals introduced by this repository. They are quarantined and
labelled `PROPOSED`. Retroactively attributing new terminology to CVLN would corrupt
the record this repository exists to protect.

## Precision over volume

Fifty accurate lines outrank three hundred speculative ones.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`
