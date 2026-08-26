---
title: Recovery Procedure
purpose: Ordered return to Normal.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: resilience/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Recovery Procedure — TARGET

1. Boot in `Recovery`; refuse new autonomous actions.
2. Integrity scan of journals and spools.
3. Ordered replay of spooled events; conflicts written to a conflict report.
4. Re-probe providers; rebuild the routing table.
5. Human review of the conflict report — a human decision of record is required to
   promote to `Normal` when conflicts existed (D-003).
6. Emit an evidence package describing the recovery (`proof/EVIDENCE-PACKAGE.md`).
