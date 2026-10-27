# 14 — Operations, incident response, professional partnerships

## Service ownership

Set a named person as security/incident owner and another as veterinary content approver. Even solo projects need a responsible escalation pathway. Do not advertise emergency service availability unless a human-backed process exists. Public support copy should explain Bhow is a record/education tool, not a staffed emergency dispatch.

## Operational runbooks to create

- **Outage:** identify failing endpoint and user impact, stop risky feature if necessary, show `Unavailable`, restore previous release, communicate status without leaking personal data.
- **Clinical content issue:** immediately disable affected KB entry/model rule, preserve version and offending outputs privately for investigation, vet review, regression test, publish corrected notice if needed.
- **Security event:** revoke tokens/shares, assess affected data, preserve audit logs, engage incident counsel, comply with applicable reporting requirements and user notifications, revalidate backups.
- **Lost dog report abuse (later):** suspend public visibility, preserve evidence privately, restrict reporter, forward only to authorized operations.
- **Provider outage:** weather, directory, SMS, push and AI degrade gracefully; stale data prominently labeled, never substituted with invented data.

## Observability requirements

Instrument API request ID, status, latency, error category, external provider latency, database pool and model failure rate. Exclude raw notes, scans, token claims, exact location and images. Adopt OpenTelemetry and protected alerting after hosting decision. Distinguish user action complete vs notification merely queued vs successfully delivered.

## Backup, restore and data portability

Managed PostgreSQL encrypted backup plus daily backup status alert. Quarterly restoration exercise into isolated environment, verify row counts/ACLs and file references. Encryption-key ownership defined. Later S3 asset versioning/deletion retention must match account erasure policy. Document RPO/RTO *after* measured test, not wishful numbers.

## Vet and welfare partnership process

Ask professional for registration credentials and scope; define approvals, prohibited claims, review fees, version/expiry requirements. A participating veterinarian verifies **specific care events**, not the entire AI application. An NGO needs case triage hours, accepted geographic area, consent terms, escalation and closed-loop status definitions. A stale listing or social-media address does not make a verified service.

## External vendor due diligence

For identity provider, SMS/FCM, object store, OCR and weather directory: pricing, DPA, region/data residency, retention, breach notice, availability, commercial licensing, permitted uses, API limits, bulk export/deletion, vendor lock-in and incident contact. Keep an internal contract/source ledger.
