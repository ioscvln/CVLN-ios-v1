---
title: Notarial Boundary
purpose: Separation of digital evidence from legal attestation.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# Notarial Boundary

| Dimension | Digital evidence (in scope) | Legal attestation (out of scope) |
|---|---|---|
| Producer | CVLN Intelligence OS | Competent authority or notary |
| Object | Integrity and attribution of records | Legal effect of an act |
| Verification | Cryptographic recomputation | Legal procedure |
| Failure mode | Chain breaks, verification fails | Instrument void |
| Status in corpus | `PARTIAL` / `TARGET` | Permanently out of scope |

The word "notary" in the audited MetaCVLN code names a **signing key role**. It does not
denote a legal notary. Decision: D-007.
