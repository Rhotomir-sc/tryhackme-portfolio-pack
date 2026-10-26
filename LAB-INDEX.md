# Lab index — evidence first

This index helps a reviewer inspect the **12 documented TryHackMe labs** without scrolling through every report. Each lab README explains the task, tools, observations and analyst limitations. The evidence index identifies the existing supporting material.

| Lab | Security question | Evidence |
|---|---|---|
| [01 · Linux identities](portfolio-labs/01-linux-user-management/README.md) | How are users, groups and protected account files inspected? | [Evidence index](portfolio-labs/01-linux-user-management/evidence-index.md) |
| [02 · Least privilege](portfolio-labs/02-linux-permissions-and-least-privilege/README.md) | What changes when unnecessary file permissions are removed? | [Evidence index](portfolio-labs/02-linux-permissions-and-least-privilege/evidence-index.md) |
| [03 · Wireshark](portfolio-labs/03-wireshark-traffic-analysis/README.md) | Which FTP and HTTP observations deserve follow-up? | [Evidence index](portfolio-labs/03-wireshark-traffic-analysis/evidence-index.md) |
| [04 · Nmap discovery](portfolio-labs/04-nmap-host-discovery/README.md) | How do discovery probes change the observed host set? | [Evidence index](portfolio-labs/04-nmap-host-discovery/evidence-index.md) |
| [05 · Web log analysis](portfolio-labs/05-log-analysis-basics/README.md) | Which Apache log records warrant investigation? | [Evidence index](portfolio-labs/05-log-analysis-basics/evidence-index.md) |
| [06 · SIEM alert triage](portfolio-labs/06-siem-alert-triage/README.md) | What supports the scheduled-task alert, and what remains unproven? | [Evidence index](portfolio-labs/06-siem-alert-triage/evidence-index.md) |
| [07 · Incident response](portfolio-labs/07-incident-response-journal/README.md) | How do process, macro, network and persistence evidence guide response? | [Evidence index](portfolio-labs/07-incident-response-journal/evidence-index.md) |
| [08 · Threat intelligence](portfolio-labs/08-threat-intelligence-ioc-analysis/README.md) | How do hashes and sandbox reports enrich analysis? | [Evidence index](portfolio-labs/08-threat-intelligence-ioc-analysis/evidence-index.md) |
| [09 · Windows telemetry](portfolio-labs/09-windows-event-log-analysis/README.md) | How can Security events, Sysmon and PowerShell history support an investigation? | [Evidence index](portfolio-labs/09-windows-event-log-analysis/evidence-index.md) |
| [10 · Cloud identity](portfolio-labs/10-cloud-identity-basics/README.md) | What links failed and successful Microsoft Entra ID sign-ins? | [Evidence index](portfolio-labs/10-cloud-identity-basics/evidence-index.md) |
| [11 · Firewall audit](portfolio-labs/11-firewall-rule-audit/README.md) | Which rule settings broaden administrative access? | [Evidence index](portfolio-labs/11-firewall-rule-audit/evidence-index.md) |
| [12 · Phishing](portfolio-labs/12-phishing-detection/README.md) | Can authenticated sender infrastructure still be used for impersonation? | [Evidence index](portfolio-labs/12-phishing-detection/evidence-index.md) |

## Three useful starting points

**Cloud and identity:** [Lab 10](portfolio-labs/10-cloud-identity-basics/README.md) — investigation of sign-in events in a training environment. Its [timeline follow-up](portfolio-labs/10-cloud-identity-basics/timeline-review.md) explicitly separates source correlation from chronological proof; the follow-up query has **not** yet been rerun.

**SOC and detection:** [Lab 06](portfolio-labs/06-siem-alert-triage/README.md) — scheduled-task alert triage using event and process evidence. A task's existence does not prove a downloaded payload executed.

**Incident response:** [Lab 07](portfolio-labs/07-incident-response-journal/README.md) — process, document, network and registry-persistence investigation in a lab. Recorded removal steps are not proof of long-term clean recovery.

## Reading the evidence

- **Observed:** Commands, queries, logs, screenshots and findings documented from an authorized training environment.
- **Inferred:** Analyst interpretations that require context and may have alternative explanations.
- **Not verified:** A stronger conclusion for which supporting telemetry or follow-up testing is missing.

A screenshot showing a room as completed is not equivalent to technical execution evidence. See the [documentation standard](DOCUMENTATION.md).

[Back to the portfolio](README.md) · [Google Cybersecurity portfolio](https://github.com/Rhotomir-sc/google-cybersecurity-portfolio-pack)
