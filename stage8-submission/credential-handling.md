# Credential Handling Record

Never place a reusable cleartext credential or full hash in the report, video,
public repository, or issue tracker.

| ID | Account type | Source artifact | Storage location | Report representation | Disposal action | UTC disposed |
|---|---|---|---|---|---|---|
| CRED-001 | foothold_user | candidate.json | encrypted local evidence directory | `[REDACTED:6ab0]` | Credential material came only from assigned lab, not tested against other systems | 2026-08-24T22:05:00Z |
| CRED-002 | service_user | candidate.json | encrypted local evidence directory | `[REDACTED:6ab0]` | Credential material came only from assigned lab, not tested against other systems | 2026-08-24T22:05:00Z |

Record cracking method parameters without publishing the recovered value. The
grader may inspect the sealed local value during defense; it is not uploaded.

I confirm the credential material came only from the assigned lab and was not
tested against any other system.

Signed: UBI-2026-0105
UTC date/time: 2026-08-24T22:05:00Z
