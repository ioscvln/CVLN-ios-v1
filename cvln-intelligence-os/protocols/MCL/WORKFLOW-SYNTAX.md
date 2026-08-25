---
title: MCL Workflow Syntax (PROPOSED)
purpose: Sketch a proposed MCL facility.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# MCL Workflow Syntax (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mcl
workflow weekly_drop_report {
  objective   "Publish the weekly drop report"
  trigger     schedule("weekly")
  gate        level(2)
  steps {
    execute report.weekly_drop by AGT-014
    observe  outcome
    report   signed
  }
  on_failure  escalate to decision
}
```

Compare `/api/cron/weekly-drop-report` and `/reports/weekly-drop`, which implement
this workflow imperatively today.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0008`
