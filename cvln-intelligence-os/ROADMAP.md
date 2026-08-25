---
title: Roadmap
purpose: Roadmap of the CVLN Intelligence OS specification.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Roadmap

Sequenced by dependency, from [`audit/GAP-ANALYSIS.md`](audit/GAP-ANALYSIS.md).

## Now — no founder decision required

1. `G-002` Implement `GET /api/capabilities` in Agent Factory and Laurentia.
2. `G-005` Encrypt the notary private key at rest, then rotate.
3. `G-003` Adopt `contracts.py::Event` as the shared envelope, signing mandatory.
4. `G-007` Add an `ARCHITECTURE.md` to every repository.

## Next — blocked on founder decisions

5. `FD-002` Ratify or abandon the canonical dependency direction.
6. `FD-001` Settle doctrine ownership and the Brain boundary.
7. `FD-004` Settle model router ownership; remove Laurentia's single point of failure.
8. `FD-003` Execute or restate the open-core split.

## Later

9. `G-004` Extract the Brain service.
10. `G-001` Wire Laurentia to the agent runtime.
11. `G-013` Propagate a trace identifier estate-wide.
12. `G-010` Specify and implement the memory graph.

## Undecided

13. `FD-005` ISA and MCL adoption. Rejection is an acceptable outcome.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`
