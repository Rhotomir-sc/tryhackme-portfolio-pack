# 10 - Cloud Identity Basics

**Evidence update:** the original searches establish a user/IP correlation, but not the order of failure and success events. The reported 26 events are *nonzero error-code events aggregated by user*, not 26 confirmed incorrect passwords from one IP. The [timeline validation guide and tested offline tool](timeline-review.md) document what still needs to be checked against the original training data.

[Timeline verification follow-up](timeline-review.md) separates source correlation from proof of chronological order. The follow-up query has not been rerun against the training dataset.


[Command/query reference](command-reference.md).


## At a glance

**Question:** What connects failed and successful cloud sign-ins?

**Evidence:** [Existing evidence index](evidence-index.md).

**Limit:** Source correlation alone does not prove event order, MFA completion, or compromise.


| Information | Details |
|---|---|
| Difficulty | Beginner |
| Category | Cloud Identity & Authentication Security |
| Platform | TryHackMe |
| Practice Room | M365 Monitoring Basics |
| Technologies | Microsoft Entra ID, Microsoft 365, Splunk |

---

## Overview

In this lab, I investigated suspicious Microsoft Entra ID authentication activity using sign-in logs collected in Splunk.

The scenario investigation identified nonzero error-code sign-in records and successful sign-in records associated with the same source IP. The original aggregated output did **not** establish chronological order.

I used Entra ID sign-in telemetry to identify:

- the targeted user
- the source IP
- nonzero-code event totals and the need to distinguish credential errors from other interruptions
- authentication error codes
- successful sign-ins
- accessed Microsoft 365 applications
- browser-based interactive sessions
- Conditional Access status

---

## Learning Goal

My goal was to practice basic cloud identity investigation and understand how authentication logs can be used to identify a possible account compromise.

Instead of looking only at individual login events, I correlated failed and successful authentication activity using:

```text
User
+
Source IP
+
Authentication result
+
Application
```

---

## Why Entra ID Logs Matter

Microsoft Entra ID sign-in logs record authentication attempts against cloud identities.

Useful fields include:

```text
userPrincipalName
ipAddress
appDisplayName
clientAppUsed
isInteractive
status.errorCode
conditionalAccessStatus
```

These fields can help SOC analysts identify brute-force activity, suspicious successful logins, unusual applications, and identity-related security events.

---

# Investigation 1 - Nonzero Error-Code Events

I started by searching nonzero-code Entra ID sign-in events. This includes some events that are **not incorrect-password attempts**, so each error code needs separate interpretation.

```spl
index="scenario" sourcetype="azure:aad:signin" "status.errorCode"!=0
| stats count as event_count values(ipAddress) as ip_addresses
 values(appDisplayName) as applications values(status.errorCode) as errorCodes by userPrincipalName
| sort - event_count
| table applications, userPrincipalName, ip_addresses, errorCodes, event_count
```

The results identified:

```text
User:
allan.smith@finegalo.thm

Source IP:
2804:2488:7082:a4c0:fd97:b11b:9895:49c0

Application:
OfficeHome

Nonzero-code events in the user-level aggregate:
26 (not verified per IP)
```

The authentication activity also contained error codes:

```text
50126
50140
```

The user-level count and listed source IP made the activity worth further investigation. The original aggregation did not show how many code-50126 credential failures came from that IP.

![Entra failed sign-ins summary](screenshots/01-entra-failed-signins-summary.png)

---

# Investigation 2 - Successful Sign-ins From the Same IP

After identifying a source IP of interest, I searched separately for successful sign-ins from that address.

```spl
index=scenario sourcetype="azure:aad:signin"
"status.errorCode"=0
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
| stats values(ipAddress) as ip_addresses
 values(appDisplayName) as applications by userPrincipalName
| table applications, userPrincipalName, ip_addresses
```

Successful authentication activity was found for:

```text
allan.smith@finegalo.thm
```

from the same IPv6 address.

The successful sign-in results listed applications:

```text
My Profile
My Signins
OfficeHome
One Outlook Web
```

This linked the two result sets by source IP and identity. Because this query aggregated values without event timestamps, it **did not prove** that the successful sign-ins came after the credential failures.

![Successful sign-ins from reviewed IP](screenshots/02-successful-signins-from-attacker-ip.png)

---

# Investigation 3 - Interactive Cloud Sessions

I then reviewed the successful authentication events in more detail.

```spl
index=scenario sourcetype="azure:aad:signin"
"status.errorCode"=0
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
userPrincipalName="allan.smith@finegalo.thm"
| table _time userPrincipalName appDisplayName ipAddress clientAppUsed isInteractive conditionalAccessStatus
```

The resulting events showed:

```text
User:
allan.smith@finegalo.thm

Client:
Browser

Interactive:
true

Conditional Access Status:
success
```

Applications included:

```text
OfficeHome
One Outlook Web
```

![Interactive browser sign-ins](screenshots/03-interactive-browser-signins.png)

These successful interactive browser sign-ins used an IP that was also listed among nonzero-code events. The original searches did not establish event order or whether the 26 nonzero-code events all originated from this IP.

`conditionalAccessStatus=success` indicates that the Conditional Access evaluation succeeded for those sign-ins.

I did not interpret this field alone as proof that MFA was completed because the evidence reviewed in this lab did not independently confirm the MFA result.

---

# Investigation Flow

```text
26 nonzero-code events (aggregated by user)
            ↓
Target identity identified
            ↓
allan.smith@finegalo.thm
            ↓
Source IPv6 identified
            ↓
2804:2488:7082:a4c0:fd97:b11b:9895:49c0
            ↓
Successful sign-ins from same IP (chronology not verified)
            ↓
OfficeHome / Outlook / account portals
            ↓
Interactive browser sessions
            ↓
Conditional Access status reviewed
```

---

# Identity Indicators

| Type | Value |
|---|---|
| User Principal Name | `allan.smith@finegalo.thm` |
| Source IPv6 | `2804:2488:7082:a4c0:fd97:b11b:9895:49c0` |
| Nonzero-code records (user-level aggregation) | `26` — per-IP and 50126 breakdown pending |
| Application | `OfficeHome` |
| Application | `One Outlook Web` |
| Client | `Browser` |
| Interactive Login | `true` |
| Conditional Access Status | `success` |

---

# What I Practiced

During this lab, I practiced:

- analysing Microsoft Entra ID sign-in logs
- using Splunk to investigate cloud authentication
- identifying repeated failed authentication attempts
- grouping events by user and source IP
- reviewing Entra ID authentication error codes
- pivoting from failed to successful sign-ins
- identifying cloud applications accessed by an account
- reviewing interactive vs non-interactive sign-ins
- reviewing Conditional Access status
- correlating identity events using common fields
- separating observed evidence from assumptions

---

# Key Takeaways

## 1. Authentication failures become more useful when aggregated

A single failed login may be normal.

Repeated failures against the same user from the same source IP provide much stronger investigation context.

---

## 2. Failed and successful events should be correlated

The most important finding came from pivoting from:

```text
Failed authentication
```

to:

```text
Successful authentication from the same source
```

This justified event-level follow-up, but the observed shared source did not prove a failure-before-success timeline or account compromise.

---

## 3. Cloud identity investigations require application context

Successful login alone was not the end of the investigation.

The logs also showed access to:

```text
OfficeHome
One Outlook Web
My Profile
My Signins
```

This identified which applications appeared in successful sign-in records; it did not independently establish subsequent in-app actions.

---

## 4. Interactive authentication provides useful context

The successful events showed:

```text
clientAppUsed = Browser
isInteractive = true
```

This indicated interactive browser-based user sessions rather than background service authentication.

---

## 5. Conditional Access fields should be interpreted carefully

The events showed:

```text
conditionalAccessStatus = success
```

I recorded this as a successful Conditional Access evaluation.

I did not assume that MFA was successfully completed without reviewing separate MFA-specific evidence.

---

# Result

In this lab, I investigated suspicious Microsoft Entra ID authentication activity using Splunk.

The user-level search returned 26 nonzero-code sign-in records for `allan.smith@finegalo.thm` and listed the IPv6 address `2804:2488:7082:a4c0:fd97:b11b:9895:49c0`. The preserved result did **not** establish that all 26 were invalid-password attempts or that they came from this single address.

I also found successful sign-in records for that source and applications including OfficeHome and Outlook. Whether those events occurred after a specific credential-failure sequence remains to be verified by timestamps.

Finally, I reviewed the successful sessions and confirmed that they were interactive browser-based sign-ins with a successful Conditional Access status.

This lab provided practical experience using Entra ID and Splunk sign-in telemetry while identifying a crucial evidence gap: aggregation does not replace a chronological, event-level investigation.

---

## Next Step

The next portfolio lab will focus on firewall rule auditing and network access-control analysis.
