---
title: Intelligent Proof Layer
purpose: How the OS produces verifiable digital evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1
status: PARTIAL
attribution: MIXED
---

# Intelligent Proof Layer

## Purpose

Make what the system did reconstructible and tamper-evident.

## Observed

- Ed25519-signed events with a verify endpoint; tampered payloads quarantined (META).
- Notarisations with verify and export, plus a public read surface (META).
- Append-only gate journal (FACTORY).

## Not observed — TARGET

- End-to-end integrity chain across a whole evidence package (V-008).
- External time anchoring.
- Package-level export format with a stable schema.

## Hard boundary

The proof layer produces **digital evidence**. It does not produce **legal
attestation**. See `proof/NOTARIAL-BOUNDARY.md` and D-007.
