---
title: Security Baseline
purpose: Frozen security posture of the estate.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: security/
version: 1.1
status: PARTIAL
attribution: MIXED
---

# Security Baseline

## Observed (evidence-backed)

- JWT authentication with bcrypt password hashing and six roles (META `backend/server.py`).
- Ed25519 signing of events with verification and quarantine of tampered payloads.
- Notarisation with a verify endpoint and a public read surface.
- Gate system blocking critical agent actions, with an append-only journal (FACTORY).
- Provider access confined to one model-router layer (FACTORY `provider_layer.py`).

## Not observed — TARGET

- Key management: the notary private key is stored unencrypted at rest (V-001).
- Mutual authentication between layers (V-003).
- Rate limiting on public surfaces (V-006).
- Secret redaction verification in provider journals (V-005).

## Rule

Anything in the second list is `TARGET`. It must not be described elsewhere in this
corpus as an existing control.

Register: `registry/VULNERABILITY-REGISTRY.md`. Decision: D-010 / `ADR-0010`.
