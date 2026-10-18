# Cloud identity timeline — follow-up procedure

Status: **query prepared; not rerun against the original lab dataset**.

The existing aggregation connects a user and source IP with failures and successes. To verify the claimed order, inspect both statuses together in the authorized lab and preserve a chronological export:

```spl
index=scenario sourcetype="azure:aad:signin"
userPrincipalName="allan.smith@finegalo.thm"
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
| sort 0 _time
| table _time userPrincipalName ipAddress status.errorCode appDisplayName clientAppUsed isInteractive conditionalAccessStatus
```

Set and record the search time range and displayed timezone. Review nonzero error codes individually; do not assume they all mean an incorrect password.

| Check | Result |
|---|---|
| Exact failure-to-success interval | Pending timestamp review |
| Identity and source consistency | Discussed in existing report; retain underlying rows when rerun |
| MFA completion | Not established by Conditional Access success alone |
| Benign alternative | Ask whether legitimate retries or shared network context could explain the activity |
| Final escalation decision | Record after the additional evidence review |

[Existing investigation](README.md) · [Evidence index](evidence-index.md)
