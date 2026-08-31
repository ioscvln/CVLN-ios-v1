---
title: External Anchoring
purpose: How an evidence-package digest is anchored outside the estate, and what that does and does not prove.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1-patch.3
status: PARTIAL
attribution: MIXED
---

# External Anchoring

## What is anchored

The `chain_hash` of an evidence package — a SHA-256 digest over every corpus document
hash and every invariant verdict. The corpus itself is never transmitted: a calendar sees
a 32-byte digest and nothing else.

## What an OpenTimestamps proof proves

- That the digest **existed** at the moment it was accepted, and later that it was
  included in a Bitcoin block once the attestation is upgraded.
- That the anchored corpus state **has not changed** since: any edit changes the digest.

## What it does not prove — stated explicitly

| Claim | Position |
|---|---|
| Qualified electronic timestamp (eIDAS) | **No.** OpenTimestamps is not a qualified trust service. |
| Legal opposability / legal effect | **No.** `legal_effect` stays `"none"` (D-007). |
| Legal attestation of content | **No.** Digital evidence only (`proof/NOTARIAL-BOUNDARY.md`). |
| Confirmation on submission | **No.** A submitted digest is `pending` until the Bitcoin attestation is merged. |
| Full verification by the portal | **No.** The portal performs structural verification; authoritative verification is `ots verify <digest>.ots` against a Bitcoin node. |

The correct wording, used throughout this corpus and the portal, is: *independent
evidence of temporal existence and integrity*.

## Provider model

The interface is provider-neutral so a qualified authority can be **added alongside**
OpenTimestamps, never replacing it.

| Provider | Status | Meaning |
|---|---|---|
| `ots` | IMPLEMENTED | OpenTimestamps public Bitcoin calendars, no credentials required |
| `rfc3161` | TARGET | Reserved for a qualified RFC 3161 / eIDAS authority; returns `unavailable` until configured |

A future qualified anchor is recorded as a second record over the same digest, so a
package can carry both.

## States

| State | Meaning |
|---|---|
| `pending` | A calendar accepted the digest; the Bitcoin attestation is not yet merged |
| `confirmed` | The Bitcoin attestation has been merged into the stored `.ots` proof |
| `offline` | No calendar was reachable; nothing is claimed |
| `unavailable` | The requested provider has no configuration (e.g. `rfc3161`) |

Anchors are derived artefacts stored in `audit/anchors/` (`index.json` plus one `.ots`
file per digest). Losing them loses no canonical content; the corpus remains the source
of truth (D-004, D-019).

## Surfaces

`GET /api/docs/anchor/providers` · `GET /api/docs/anchors` ·
`POST /api/docs/anchor/{baseline}` · `POST /api/docs/anchor/{digest}/upgrade` ·
`GET /api/docs/anchor/{digest}/verify`. The evidence package carries the anchor record
and the base64 `.ots` proof when one exists; `anchored_at` is set only for a `confirmed`
anchor.

Decision: D-020 (`decisions/ADR-0020-D-020.md`). Configuration: `OTS_CALENDARS`,
`OTS_TIMEOUT_SECONDS`.
