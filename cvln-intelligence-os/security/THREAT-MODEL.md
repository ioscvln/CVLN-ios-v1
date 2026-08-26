---
title: Threat Model
purpose: Adversaries, assets and abuse cases.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: security/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Threat Model — TARGET

## Assets

Doctrine of record · decision journal · notary keys · agent definitions · memory graph ·
evidence packages.

## Adversaries

| Adversary | Capability | Primary target |
|---|---|---|
| External attacker | Public endpoints | Notary keys, public audit surface |
| Compromised provider | Model responses | Reasoning integrity, prompt exfiltration |
| Malicious agent definition | ADL authoring | Gate bypass, capability escalation |
| Insider with role | Governance API | Silent doctrine mutation |
| Physical/power event | Availability | Journal durability (see `resilience/POWER-LOSS.md`) |

## Abuse cases

1. Forged event accepted as signed → mitigated by Ed25519 verification (observed).
2. Notary key exfiltration → **not mitigated** (V-001).
3. Agent escalating past its gate level → mitigated by gate check (observed), unverified.
4. Evidence package altered after emission → **not mitigated end-to-end** (V-008).

Nothing in this document may be read as a deployed control.
