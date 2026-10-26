"""Offline regression tests; the fixture is synthetic, not a THM export."""
import contextlib
import io
import json
from decimal import Decimal
from pathlib import Path
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "tools"))
from validate_signin_timeline import evaluate, main, read_events

FIXTURE = LAB / "tests" / "fixtures" / "synthetic_signins.csv"
BASE = Decimal("1789027200")


def event(seconds, code, user="analyst@training.invalid", ip="2001:db8::10"):
    return {
        "time": BASE + Decimal(str(seconds)),
        "user": user,
        "ip": ip,
        "code": code,
        "app": "OfficeHome",
    }


class TimelineTests(unittest.TestCase):
    def test_synthetic_fixture_is_explicitly_separate_from_lab(self):
        rows = read_events(FIXTURE)
        report = evaluate(rows)
        self.assertEqual(report["total_rows"], 8)
        self.assertEqual(report["error_code_counts"], {
            "0": 2, "50126": 4, "50140": 1, "53003": 1
        })
        self.assertEqual(len(report["findings"]), 1)
        finding = report["findings"][0]
        self.assertEqual(finding["user"], "analyst@training.invalid")
        self.assertEqual(finding["source_ip"], "2001:db8::10")
        self.assertEqual(finding["credential_failure_count"], 3)
        self.assertEqual(finding["matching_success_utc"], "2026-09-10T08:00:20+00:00")
        self.assertIn("not_verified_lab_evidence", report["source"])

    def test_kmsi_interrupt_is_not_password_failure(self):
        rows = [event(0, 50126), event(1, 50140), event(2, 50140),
                event(3, 0)]
        self.assertEqual(evaluate(rows)["findings"], [])
        self.assertEqual(len(evaluate(rows, threshold=1)["findings"]), 1)
        self.assertEqual(evaluate(rows, threshold=1)["findings"][0]
                         ["credential_failure_count"], 1)

    def test_order_must_be_real_chronology(self):
        rows = [event(10, 50126), event(11, 50126), event(12, 50126),
                event(5, 0)]
        self.assertEqual(evaluate(rows)["findings"], [])
        rows.append(event(20, 0))
        self.assertEqual(len(evaluate(rows)["findings"]), 1)

    def test_group_by_user_and_ip(self):
        rows = [event(n, 50126) for n in (0, 1)]
        rows += [event(2, 50126, user="another@training.invalid"),
                 event(3, 50126, ip="2001:db8::20"), event(4, 0)]
        self.assertEqual(evaluate(rows)["findings"], [])

    def test_window_boundary(self):
        rows = [event(0, 50126), event(1, 50126),
                event(600, 50126), event(600, 0)]
        self.assertEqual(evaluate(rows, threshold=2)["findings"][0]
                         ["credential_failure_count"], 2)
        self.assertEqual(evaluate(rows, threshold=3)["findings"], [])

    def test_equal_timestamps_do_not_prove_order(self):
        rows = [event(0, 50126)] * 3 + [event(0, 0)]
        self.assertEqual(evaluate(rows)["findings"], [])

    def test_success_resets_sequence(self):
        rows = [event(n, 50126) for n in (0, 1, 2)] + [
            event(3, 0), event(4, 0)
        ]
        self.assertEqual(len(evaluate(rows)["findings"]), 1)

    def test_no_matching_success_and_large_threshold(self):
        self.assertEqual(evaluate([event(n, 50126) for n in range(5)])
                         ["findings"], [])
        self.assertEqual(evaluate(read_events(FIXTURE), threshold=4)
                         ["findings"], [])

    def test_invalid_thresholds_and_windows(self):
        for threshold in (0, -1, True):
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError):
                    evaluate([], threshold=threshold)
        for window in (0, "-1", "NaN", "Infinity", "bad"):
            with self.subTest(window=window):
                with self.assertRaises(ValueError):
                    evaluate([], window_minutes=window)

    def test_bad_csv_rejected(self):
        bad = [
            "some,other,header\na,b,c\n",
            "event_epoch,userPrincipalName,ipAddress,status.errorCode,appDisplayName\n"
            "notatime,u@training.invalid,2001:db8::1,50126,OfficeHome\n",
            "event_epoch,userPrincipalName,ipAddress,status.errorCode,appDisplayName\n"
            "1789027200,u@training.invalid,not-an-ip,50126,OfficeHome\n",
            "event_epoch,userPrincipalName,ipAddress,status.errorCode,appDisplayName\n"
            "1789027200,u@training.invalid,2001:db8::1,x,OfficeHome\n",
        ]
        for sample in bad:
            with self.subTest(sample=sample[:30]):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "bad.csv"
                    path.write_text(sample, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        read_events(path)

    def test_json_cli_is_parseable(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            main(["--input", str(FIXTURE), "--format", "json"])
        result = json.loads(stream.getvalue())
        self.assertEqual(result["total_rows"], 8)
        self.assertEqual(len(result["findings"]), 1)
        self.assertEqual(result["credential_failure_code"], 50126)

    def test_missing_input_exits_with_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as cm:
                    main(["--input", str(Path(tmp) / "missing.csv")])
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
