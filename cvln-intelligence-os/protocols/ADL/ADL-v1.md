---
title: ADL v1 — Agent Definition Language
purpose: Specify the implemented CVLN agent definition language.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# ADL v1 — Agent Definition Language

ADL is the one protocol in the initial brief that demonstrably exists. Source of
truth: `FACTORY/backend/adl_schema.py`, with a second generation at
`FACTORY/backend/schemas/adl_v2_schema.json`.

## Implemented grammar

| Rule | Regex / enum | Evidence |
|---|---|---|
| Agent identifier | `^AGT-\d{3}$` | `AGENT_ID_RE` |
| Version | `^\d+\.\d+\.\d+$` | `SEMVER_RE` |
| Lifecycle | Draft, Prototype, Alpha, Beta, Production, Maintenance, Archive | `LifecycleStatus` |
| Transitions | next stage, or Archive | `allowed_transitions()` |
| Brain memory binding | `scope: session | persistent`, `owner` | `BrainMemory` |
| Brain events binding | `subscribe: []`, `publish: []` | `BrainEvents` |

YAML is a first-class input format via `parse_adl_yaml()`.

## Example agent definition (v1 shape)

```yaml
agent_id: AGT-014
name: Weekly Drop Reporter
version: 1.2.0
lifecycle_status: Production
autonomy_level: 2
risk_level: medium
brain:
  memory:
    scope: persistent
    owner: AGT-014
  events:
    subscribe: ["daily.closing.completed"]
    publish: ["agent.report.ready"]
capabilities:
  - id: report.weekly_drop
    gate_level: 2
```

## Example v2 envelope

```yaml
adl_version: "2.0"
schema_uri: "https://cvln.spec/adl/v2.json"
agent:
  id: AGT-014
  name: Weekly Drop Reporter
brain:
  memory: { scope: persistent }
capabilities:
  - id: report.weekly_drop
```

## Known issue

v1 and v2 coexist with no declared authoritative version and no converter
(`G-016`). Fields not present in either schema are `PROPOSED`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`
