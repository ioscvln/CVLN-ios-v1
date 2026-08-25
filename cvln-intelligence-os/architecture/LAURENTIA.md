---
title: Laurentia
purpose: Specify the cultural-industry operator as audited.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Laurentia

Layer 3. Purpose: cultural-industry operator — conversations, workflows, reports,
artefacts, sessions, jobs.

## Implemented subsystems

Gateway with SSE token streaming · Brain interface and persona · local orchestrator
with circuit breaker and signals · cookieless HMAC-SHA256 ghost persistence ·
AES-256-GCM encryption at rest · MongoDB TTL sliding-window rate limiting without
Redis · RGPD D+90 purge of the identity mapping · omnichannel echo pipeline
(Instagram, LinkedIn, X) · signed PDF export with QR · file parsing · Stripe billing ·
multi-tenant instance factory and API keys · bridges to Kiltikonet, LabelOS, FREKCORE.

## Distinctive properties

Laurentia is the only audited system with encryption at rest, bounded retention and a
paying commercial surface. Its privacy engineering is the estate's strongest.

## Rule violations recorded

It owns a persona-level doctrine (`C-002`), hardcodes a single provider with no
fallback (`C-004`, `G-011`), and its README describes an open-core split that has not
been performed (`C-003`).

## Not implemented

Any consumption of Agent Factory or META. Laurentia is a complete product that is not
yet a layer.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
