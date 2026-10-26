"""Validate time order in exported Splunk/Entra sign-in events (offline).

Input must have epoch seconds in "event_epoch", not a locale-formatted "_time".
This utility does not query Splunk or establish account compromise.
"""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from ipaddress import ip_address
import json
from pathlib import Path

REQUIRED = {
    "event_epoch", "userPrincipalName", "ipAddress",
    "status.errorCode", "appDisplayName",
}
BAD_PASSWORD = 50126
KMSI_INTERRUPT = 50140


def read_events(path):
    """Parse a CSV export; reject missing data or ambiguous timestamps."""
    events = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)) or not REQUIRED.issubset(fields):
            raise ValueError("CSV needs unique columns: " + ", ".join(sorted(REQUIRED)))
        for number, row in enumerate(reader, 2):
            try:
                if None in row or any(row.get(key) is None for key in REQUIRED):
                    raise ValueError("wrong number of columns")
                raw = {k: str(row[k]).strip() for k in REQUIRED}
                if not all(raw.values()):
                    raise ValueError("empty required field")
                instant = Decimal(raw["event_epoch"])
                if not instant.is_finite() or not 0 <= instant <= 32503680000:
                    raise ValueError("event_epoch must be a finite, valid UNIX time")
                # Ensure the timestamp is also representable as a UTC date.
                datetime.fromtimestamp(float(instant), tz=timezone.utc)
                code = int(raw["status.errorCode"])
                if code < 0:
                    raise ValueError("negative error code")
                events.append({
                    "time": instant,
                    "user": raw["userPrincipalName"].casefold(),
                    "ip": str(ip_address(raw["ipAddress"])),
                    "code": code,
                    "app": raw["appDisplayName"],
                })
            except (InvalidOperation, ValueError, OverflowError, TypeError) as exc:
                raise ValueError(f"Invalid row {number}: {exc}") from exc
    return events


def utc_string(epoch):
    return datetime.fromtimestamp(float(epoch), tz=timezone.utc).isoformat()


def evaluate(events, threshold=3, window_minutes=10):
    """A 50126-only failure sequence must precede success for the same pair.

    A 50140 interrupt is not a password failure. Equal timestamps are
    ambiguous and never qualify as failure-before-success. Each success
    resets the sequence for its user and IP.
    """
    if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 1:
        raise ValueError("threshold must be a positive integer")
    try:
        window = Decimal(str(window_minutes)) * 60
    except InvalidOperation as exc:
        raise ValueError("invalid window") from exc
    if not window.is_finite() or window <= 0:
        raise ValueError("window must be positive and finite")

    ordered = sorted(events, key=lambda e: e["time"])
    failures = defaultdict(list)
    findings = []
    for event in ordered:
        key = (event["user"], event["ip"])
        queue = failures[key]
        # Remove stale failures for every event, not only successes.
        queue[:] = [old for old in queue if event["time"] - old["time"] <= window]
        if event["code"] == BAD_PASSWORD:
            queue.append(event)
        elif event["code"] == 0:
            earlier = [old for old in queue if old["time"] < event["time"]]
            if len(earlier) >= threshold:
                findings.append({
                    "user": key[0],
                    "source_ip": key[1],
                    "credential_failure_count": len(earlier),
                    "first_credential_failure_utc": utc_string(earlier[0]["time"]),
                    "matching_success_utc": utc_string(event["time"]),
                    "matching_success_application": event["app"],
                    "assessment": "review_required_not_confirmed_compromise",
                })
            queue.clear()

    counts = Counter(e["code"] for e in events)
    return {
        "source": "supplied_csv_export_not_verified_lab_evidence",
        "total_rows": len(events),
        "error_code_counts": {str(code): counts[code] for code in sorted(counts)},
        "credential_failure_code": BAD_PASSWORD,
        "excluded_interrupt_code": KMSI_INTERRUPT,
        "threshold": threshold,
        "window_minutes": float(window / 60),
        "findings": findings,
        "limitations": [
            "A nonzero error code is not always a wrong password.",
            "Finding(s) do not establish unauthorized access or MFA completion.",
            "Events with equal timestamps do not establish a sequence.",
            "Export may omit records; duplicates may inflate counts.",
            "Validation of the original training lab requires its real event-level export.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="CSV with event_epoch field")
    parser.add_argument("--threshold", type=int, default=3)
    parser.add_argument("--window-minutes", type=str, default="10")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        report = evaluate(read_events(args.input), args.threshold, args.window_minutes)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
        return
    print("Cloud identity event timeline — offline verification")
    print(f"Event rows: {report['total_rows']}")
    print("Error-code counts:", report["error_code_counts"])
    print("50126 = credential validation failure; 50140 = KMSI interrupt (excluded)")
    print(f"Matches requiring review: {len(report['findings'])}")
    for finding in report["findings"]:
        print(f"  {finding['user']} ({finding['source_ip']}): "
              f"{finding['credential_failure_count']} credential failures before "
              f"{finding['matching_success_utc']}")
    print("Results are review leads; not proof of compromise.")


if __name__ == "__main__":
    main()
