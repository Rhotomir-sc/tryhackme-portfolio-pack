# Commands and queries

Extracted from the existing report for review. These are reference snippets, not a new execution record. Use the original lab context; results depend on its dataset and environment.

## Snippet 1

```spl
index="scenario" sourcetype="azure:aad:signin" "status.errorCode"!=0
| stats count as event_count values(ipAddress) as ip_addresses
 values(appDisplayName) as applications values(status.errorCode) as errorCodes by userPrincipalName
| sort - event_count
| table applications, userPrincipalName, ip_addresses, errorCodes, event_count
```

## Snippet 2

```spl
index=scenario sourcetype="azure:aad:signin"
"status.errorCode"=0
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
| stats values(ipAddress) as ip_addresses
 values(appDisplayName) as applications by userPrincipalName
| table applications, userPrincipalName, ip_addresses
```

## Snippet 3

```spl
index=scenario sourcetype="azure:aad:signin"
"status.errorCode"=0
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
userPrincipalName="allan.smith@finegalo.thm"
| table _time userPrincipalName appDisplayName ipAddress clientAppUsed isInteractive conditionalAccessStatus
```


## Snippet 4 — event-level export for chronology verification (not yet rerun)

The earlier `stats values(...)` queries summarize fields but do not preserve the ordering of individual failed and successful sign-ins. The follow-up below is **prepared only**, not executed on the original room dataset:

```spl
index=scenario sourcetype="azure:aad:signin"
userPrincipalName="allan.smith@finegalo.thm"
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
| eval event_epoch=_time
| table event_epoch userPrincipalName ipAddress status.errorCode appDisplayName clientAppUsed isInteractive conditionalAccessStatus
| sort 0 event_epoch
```

Retain each event's `status.errorCode`; distinguish `50126` incorrect credentials from `50140` Keep me signed in interrupt. [Export procedure and tested offline validator](timeline-review.md).

[Investigation](README.md)
