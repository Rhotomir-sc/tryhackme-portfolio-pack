# TryHackMe — Defensive Security Portfolio

**12 documented labs · Linux · Network Analysis · SOC/IR · Cloud Identity**

This repository contains my hands-on cybersecurity investigations in authorized TryHackMe training environments. The emphasis is on **the question investigated, evidence collected, interpretation and limitations** — not room-completion badges.

## Start here

- **[All 12 labs and their evidence](LAB-INDEX.md)** — one-page index linking every investigation and its evidence.
- **[Cloud identity sign-in analysis](portfolio-labs/10-cloud-identity-basics/README.md)** — Microsoft Entra ID / Microsoft 365 events investigated with Splunk; includes an explicit [timeline verification gap](portfolio-labs/10-cloud-identity-basics/timeline-review.md).
- **[SIEM alert triage](portfolio-labs/06-siem-alert-triage/README.md)** — suspicious scheduled-task activity and the limits of what process telemetry establishes.
- **[Incident response journal](portfolio-labs/07-incident-response-journal/README.md)** — a Windows malware scenario involving process activity, network attempts, macro behavior and registry persistence.

## Work by area

| Area | Labs |
|---|---|
| Linux and access control | [Users and groups](portfolio-labs/01-linux-user-management/README.md) · [Permissions](portfolio-labs/02-linux-permissions-and-least-privilege/README.md) |
| Network analysis | [Wireshark](portfolio-labs/03-wireshark-traffic-analysis/README.md) · [Nmap](portfolio-labs/04-nmap-host-discovery/README.md) |
| SOC and logs | [Apache logs](portfolio-labs/05-log-analysis-basics/README.md) · [Splunk triage](portfolio-labs/06-siem-alert-triage/README.md) · [Windows and Sysmon](portfolio-labs/09-windows-event-log-analysis/README.md) |
| Incident investigation | [Incident response](portfolio-labs/07-incident-response-journal/README.md) · [Threat intelligence](portfolio-labs/08-threat-intelligence-ioc-analysis/README.md) |
| Identity and access | [Cloud sign-ins](portfolio-labs/10-cloud-identity-basics/README.md) · [Windows firewall](portfolio-labs/11-firewall-rule-audit/README.md) |
| Email security | [Phishing analysis](portfolio-labs/12-phishing-detection/README.md) |

## Investigation approach

**Observe → collect → correlate → evaluate → document.**

For each lab, I record the technical evidence and distinguish what it **shows** from what it **might mean**. For example, an HTTP 200 response is not proof of an authenticated session, and a successful sign-in from an IP associated with failed attempts does not independently prove compromise.

Each lab includes an [evidence index](LAB-INDEX.md). Screenshots are selected for technical value; historical completion images are not presented as investigation proof. See the [documentation standard](DOCUMENTATION.md).

## Current direction

I am developing deeper skills in **Microsoft Entra ID, IAM, cloud security, SOC detection and incident response**, with controlled offensive-security practice to understand attacker techniques and improve defensive reasoning.

Related work: [Google Cybersecurity certificate portfolio](https://github.com/Rhotomir-sc/google-cybersecurity-portfolio-pack) · [Security capstone](https://github.com/Rhotomir-sc/security-capstone) · [Academic work](https://github.com/Rhotomir-sc/semester-evidence-packs).

*Training environments only. Any unverified follow-up or planned task is identified rather than presented as completed work.*
