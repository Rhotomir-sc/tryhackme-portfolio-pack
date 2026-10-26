# Evidence index

References below identify the existing report illustrations; they are not a new visual verification of their contents.

| Report reference | File |
|---|---|
| Entra failed sign-ins summary | [Open image](screenshots/01-entra-failed-signins-summary.png) |
| Successful sign-ins from attacker IP | [Open image](screenshots/02-successful-signins-from-attacker-ip.png) |
| Interactive browser sign-ins | [Open image](screenshots/03-interactive-browser-signins.png) |


## Reproducible follow-up (separate from original screenshots)

- [Timeline export and validation workflow](timeline-review.md) — proposed authorized Splunk rerun; original event-level export **not obtained**.
- [Offline validator source](tools/validate_signin_timeline.py) — chronological classification of `50126`, `50140` and code-0 success events from a CSV export.
- [Automated tests](tests/test_timeline_validator.py) and [synthetic fixture](tests/fixtures/synthetic_signins.csv) — test data and code behavior, **not new evidence from the original lab**.

## Scope and metadata

Source correlation alone does not prove event order, MFA completion, or compromise.

The original execution date and tool versions are not consistently recorded. They are left unspecified rather than inferred from commit dates. When revisiting this lab, record date/timezone, platform/room, tool version, input source, and any redactions.

[Full investigation](README.md)
