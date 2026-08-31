---
title: Kiltikonet Security
purpose: Assets, observed controls and registered weaknesses.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Security

## Assets

Participant identities and FREK-IDs · badge records and access zones · jeton ledger ·
payment sessions · field scan history · admin and founder sessions · eight classes of
secret held in the backend environment.

## Observed controls

- JWT in httpOnly cookies (30 days), WebAuthn (Face ID / Touch ID), Google OAuth, Magic
  Link — five authentication methods on one login surface.
- Stripe-hosted payment flow with webhook verification endpoint.
- Email domain authentication (DKIM / SPF / DMARC) on transactional mail.

## Registered weaknesses

V-009 (documented admin bypass, CRITICAL), V-010 (live keys and eight secret classes in
one environment file, HIGH), V-011 (primary data mirrored to Baserow, HIGH), V-012
(client-side offline scan queue, MEDIUM) — see `registry/VULNERABILITY-REGISTRY.md`.

No vulnerability is invented: every row cites a line of the audited repository.
