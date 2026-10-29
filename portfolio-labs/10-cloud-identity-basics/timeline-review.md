# Lab 10 — Verify the cloud sign-in timeline

**Status: offline validator implemented and tested with synthetic rows; original TryHackMe dataset NOT re-queried.**

## Why this follow-up matters

The original [lab report](README.md) identified a user, an IPv6 source and both nonzero-code and successful sign-in records. The initial `stats values(...)` searches are **aggregations without chronological event rows**.

- The reported **26** is a count of nonzero-code records grouped by `userPrincipalName` in the original search. It is **not a verified count of wrong passwords** or a confirmed count for a *single* IP, because that search did not group by IP.
- `AADSTS50126` represents a username/password validation failure.
- `AADSTS50140` represents a **Keep me signed in (KMSI) interrupt**, not an incorrect-password verdict.
- The successful sign-ins from the same source are documented, but the original search does not establish the **relative time order**.
- `conditionalAccessStatus=success` alone does not establish MFA completion or unauthorized access.

Microsoft's code definitions: [Entra authentication error reference](https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes). Splunk stores the event `_time` timestamp as [UNIX epoch time](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.6/time-format-variables-and-modifiers/time-modifiers).

## Step 1 — Rerun the event-level search

In the **authorized M365 Monitoring Basics room** use the original Splunk instance and set the relevant search-time range. Record the chosen range and tool/session timezone. Do **not** fabricate the dates.

```spl
index=scenario sourcetype="azure:aad:signin"
userPrincipalName="allan.smith@finegalo.thm"
ipAddress="2804:2488:7082:a4c0:fd97:b11b:9895:49c0"
| eval event_epoch=_time
| table event_epoch userPrincipalName ipAddress status.errorCode appDisplayName clientAppUsed isInteractive conditionalAccessStatus
| sort 0 event_epoch
```

The `event_epoch` field retains a machine-readable timestamp independent of how Splunk displays local dates. Do not aggregate with `stats values(...)` for this task: retain **one row per event**, including 0, 50126, 50140 and any other codes.

**Export the result as CSV.** Confirm its headers contain:

```text
event_epoch,userPrincipalName,ipAddress,status.errorCode,appDisplayName
```

Other columns are allowed. Do not commit an unreviewed lab/tenant export, access tokens or personal identifiers. Keep any permitted original export locally and record its provenance separately.

## Step 2 — Run the offline validator

From the repository root, Python 3.10+ (no external packages):

```sh
python portfolio-labs/10-cloud-identity-basics/tools/validate_signin_timeline.py --input path/to/authorized-export.csv --format json
```

The tool parses UNIX timestamps, groups events by **user + IP**, sorts chronologically, and looks for **three or more 50126 errors followed by a later code-0 success within ten minutes**.

It **does not** count 50140 (KMSI) as an incorrect-password event. Other nonzero codes are included in the summary but not assumed to be wrong-password attempts. Each success resets that user's/source's pending failure sequence. Equal-time events do not prove order.

Change the threshold or time window, if necessary, with `--threshold N --window-minutes M`. A result is an **investigation lead**, not a breach verdict.

### Share a review summary without raw user and IP fields

If you need to show the analysis output in a public portfolio, add `--redact-identifiers`:

```sh
python portfolio-labs/10-cloud-identity-basics/tools/validate_signin_timeline.py --input path/to/authorized-export.csv --format json --redact-identifiers
```

This replaces finding-level user and source-IP values with `user_1`, `source_1`, and similar labels, consistently within a single report. **This is not full anonymization**: event times, application names, counts and the scenario description can still reveal context. Review the result carefully before publishing, and do not commit the raw export.

## Step 3 — Validate the tool using synthetic data (available now)

This exercise can be reproduced today without access to TryHackMe:

```sh
python portfolio-labs/10-cloud-identity-basics/tools/validate_signin_timeline.py --input portfolio-labs/10-cloud-identity-basics/tests/fixtures/synthetic_signins.csv
python -m unittest discover -s portfolio-labs/10-cloud-identity-basics/tests -v
```

The fixture uses the documentation IPv6 block `2001:db8::/32` and `training.invalid` identities. Its eight artificial rows include three credential failures, one 50140 interruption, and a later success for the same user/source. The expected result is **one synthetic review finding**. These results are **not** evidence of what occurred in the original room.

The unit tests also cover event order, source separation, timestamp ties, window boundaries, invalid timestamps, malformed CSV and absence of a matching success.

## Verification record — still pending real room access

| Check | Current status |
|---|---|
| Preserve original Splunk search-range and export context | Pending |
| Confirm event-level error-code counts for the account and exact IP | Pending |
| Establish first/last 50126 times and the first later code-0 success | Pending |
| Distinguish 50140 and other nonzero codes | Supported in code; original data pending |
| Verify successful app sign-ins after failures using timestamps | Pending |
| Confirm MFA or identity-owner authorization | Not established |
| Evaluate whether to escalate | Pending original event-level evidence |

When revisiting the room, note the lab date, search range, result timezone, actual rows, an alternative benign explanation, and any unavailable fields. Add only evidence you actually capture and are permitted to share.

**Interpretation boundary:** A matching sequence justifies further triage. It does not prove one attacker, session ownership, MFA completion, or confirmed account compromise.

[Original lab report](README.md) · [Command reference](command-reference.md) · [Evidence index](evidence-index.md)
