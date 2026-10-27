# 20 — Threat model (initial STRIDE-style)

## Assets and trust boundaries

Assets: dog/caregiver relationship, notes, future medical records, future photos, future precise location, authenticated tokens, private share grants, veterinary attestations, rescue partner routing. Boundary: Flet client is untrusted; all client fields validated by server; JWT identity is only from trusted OIDC issuer; health sources are untrusted until approved; data from ML/OCR is an untrusted suggestion.

| Threat | Attack path | Current mitigation | Required before launch |
|---|---|---|---|
| IDOR / unauthorized reading | Guess a dog UUID | Every dog query joins caregiver; 404 | Pentest nested/asset/share routes |
| Privilege escalation | Set `verified=true` as normal user | Not exposed in input schema | Secure vet-only attestation service |
| Dev identity bypass | `X-Dev-User` header | Permitted only if local+opt-in; prod startup rejects | Infrastructure guard, deployment policy |
| Expired/forged JWT | Manipulate bearer claims | RS256 signature, issuer/audience/expiry | Refresh/revocation tests, key rotation |
| Data exfil via logs | Sensitive body in tracing | No full body logging in application | Proxy/APM filtering and audits |
| Prompt injection | Untrusted uploaded vet note | No LLM pipeline at present | Structured extraction, allowlist tools, isolated sources |
| Poison-data false reassurance | OCR misses toxin | Never returns `safe` | Vet/QA corpus and confirmation UI |
| PII in QR link | Embed name/location in URL | No public sharing in MVP | Opaque scoped revocable tokens |
| Abuse of rescue reports | Fake locations/harassment | Rescue endpoint disabled | Moderation, coarse public location, reporting |
| Model data leakage | Training on private dog photos | Training pipeline not connected | Separate opt-in, provenance, revocation |
| Malicious photo upload | Oversized/malware/decompression | Upload not implemented | Private quarantine, MIME magic, AV, EXIF wipe |
| DDoS/AI cost | High-frequency public scan | Expensive scans disabled | Edge quotas, rate limits, authenticated budgets |
| Account data erasure gap | IDs/objects persist externally | MVP DB-only deletion transparent | Full deletion orchestration and attestations |

## Abuse-case tests before adding welfare features

Can a stalker recover exact animal/rescuer location from shared link, image EXIF or timeline? Can a bad actor mark rescued/captured dogs without vet authorization? Can fake clinics appear as 24-hour providers? Can another user query an image hash or notification token to infer identity? Can spoofed “vet-verified” records be submitted by a user? These are foundational go/no-go cases, not edge polish.

<!-- STRIDE threat analysis review: complete -->
