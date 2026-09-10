# TryHackMe Cybersecurity Portfolio

This repository documents my hands-on cybersecurity practice through TryHackMe labs.

Instead of using the repository as a list of completed rooms, I use each lab to document a specific security task, the evidence I collected, the tools I used, and the conclusions I reached.

The portfolio currently focuses on defensive security, SOC analysis, incident response, network analysis, Windows telemetry, threat intelligence, cloud identity, and access control.

---

## Portfolio Focus

My main technical direction is:

```text
Cloud Security
+
Identity Security
+
SOC / Incident Response
```

I am building this foundation through practical work in:

- Linux administration and access control
- network discovery and packet analysis
- log analysis and SIEM investigation
- Windows event and Sysmon analysis
- incident response
- threat intelligence
- Microsoft Entra ID authentication monitoring
- firewall auditing
- phishing analysis

I also study offensive security fundamentals to better understand attacker behaviour from a defensive perspective.

---

# Portfolio Labs

The repository contains 12 completed hands-on labs.

Each lab has its own README and selected screenshots that show actual investigation or technical work.

## Linux & Access Control

### [01 - Linux User Management](portfolio-labs/01-linux-user-management)

Practice with Linux user creation, group membership, and account verification.

### [02 - Linux Permissions and Least Privilege](portfolio-labs/02-linux-permissions-and-least-privilege)

Reviewing Linux file permissions and applying least-privilege changes.

---

## Network Discovery & Packet Analysis

### [03 - Wireshark Traffic Analysis](portfolio-labs/03-wireshark-traffic-analysis)

Analysing FTP and HTTP traffic with Wireshark filters and reviewing protocol behaviour.

### [04 - Nmap Host Discovery](portfolio-labs/04-nmap-host-discovery)

Comparing Nmap discovery methods and identifying live hosts and exposed services.

---

## SOC & Log Analysis

### [05 - Log Analysis Basics](portfolio-labs/05-log-analysis-basics)

Analysing Apache logs with command-line tools to identify HTTP errors, request patterns, and suspicious endpoints.

### [06 - SIEM Alert Triage](portfolio-labs/06-siem-alert-triage)

Investigating a Windows scheduled-task alert in Splunk and distinguishing observed evidence from assumptions.

### [09 - Windows Event Log Analysis](portfolio-labs/09-windows-event-log-analysis)

Correlating Windows Security logs, Sysmon telemetry, DNS activity, process behaviour, persistence, and PowerShell history.

---

## Incident Response & Threat Intelligence

### [07 - Incident Response Journal](portfolio-labs/07-incident-response-journal)

Following a Windows malware incident through detection, analysis, containment, eradication, and recovery.

### [08 - Threat Intelligence & IOC Analysis](portfolio-labs/08-threat-intelligence-ioc-analysis)

Using SHA-256 hashes, sandbox intelligence, network indicators, malware classification, and MITRE ATT&CK mappings.

### [12 - Phishing Detection](portfolio-labs/12-phishing-detection)

Analysing a suspicious email through sender information, URLs, message headers, and SPF/DKIM/DMARC interpretation.

---

## Cloud, Identity & Security Engineering

### [10 - Cloud Identity Basics](portfolio-labs/10-cloud-identity-basics)

Investigating Microsoft Entra ID sign-in logs in Splunk and correlating failed and successful cloud authentication activity.

### [11 - Firewall Rule Audit](portfolio-labs/11-firewall-rule-audit)

Auditing Windows Defender Firewall profiles and identifying overly permissive remote-management rules.

---

# Skills Demonstrated

Across the labs, I practiced:

- Linux user and permission management
- least-privilege access control
- Wireshark packet filtering
- Nmap host discovery
- Apache log analysis
- Splunk searches and SIEM triage
- Windows Security Event analysis
- Sysmon telemetry analysis
- parent-child process investigation
- PowerShell history review
- incident response workflows
- IOC collection and enrichment
- SHA-256 hashing
- malware sandbox analysis
- MITRE ATT&CK mapping
- Microsoft Entra ID sign-in analysis
- authentication failure investigation
- cloud identity correlation
- Windows firewall auditing
- phishing email analysis
- SPF, DKIM, and DMARC interpretation

---

# Investigation Approach

I try to follow the same basic workflow throughout the repository:

```text
Observe
   ↓
Collect Evidence
   ↓
Correlate
   ↓
Analyse
   ↓
Document
```

A major focus of the portfolio is separating:

```text
Observed Evidence
```

from:

```text
Assumptions
```

For example, I avoid labeling unusual network traffic as confirmed command-and-control unless the evidence supports that conclusion.

---

# Evidence Policy

This repository is not intended to be a TryHackMe screenshot archive.

Screenshots are included only when they demonstrate useful technical evidence, such as:

- commands I executed
- filters I applied
- process or log findings
- network indicators
- persistence mechanisms
- remediation actions
- authentication evidence
- configuration findings

Theory pages, room completion screens, and repetitive screenshots are intentionally excluded.

---

# Google Cybersecurity Connection

Some labs connect to topics covered in the Google Cybersecurity Certificate.

When relevant, individual lab READMEs include a short **Google Cybersecurity Connection** section explaining how I reinforced course concepts through hands-on practice.

The Google course material itself is documented separately rather than duplicated inside this TryHackMe repository.

---

# CTF Practice

The [`ctf-practice`](ctf-practice) directory contains additional challenge-based practice.

The goal is to improve:

- problem solving
- technical investigation
- command-line confidence
- offensive-security awareness

It is kept separate from the main portfolio labs because the portfolio labs focus more strongly on structured defensive-security documentation.

---

# Learning Journal

The [`learning-journal`](learning-journal) directory is used for short notes and progress tracking.

It is separate from the polished portfolio labs so that the main lab folders remain focused on completed technical work.

---

# Repository Structure

```text
tryhackme-portfolio-pack/
│
├── portfolio-labs/
│   ├── 01-linux-user-management/
│   ├── 02-linux-permissions-and-least-privilege/
│   ├── 03-wireshark-traffic-analysis/
│   ├── 04-nmap-host-discovery/
│   ├── 05-log-analysis-basics/
│   ├── 06-siem-alert-triage/
│   ├── 07-incident-response-journal/
│   ├── 08-threat-intelligence-ioc-analysis/
│   ├── 09-windows-event-log-analysis/
│   ├── 10-cloud-identity-basics/
│   ├── 11-firewall-rule-audit/
│   └── 12-phishing-detection/
│
├── ctf-practice/
├── learning-journal/
└── README.md
```

---

# Current Direction

The 12-lab foundation in this repository is complete.

My next technical focus is to go deeper into:

```text
Microsoft Entra ID
IAM
Cloud Security
SOC / Incident Response
```

and later connect these areas with:

```text
AI Security
```

The goal is to continue moving from beginner labs toward more realistic security investigations, cloud identity scenarios, and larger end-to-end projects.

---

# Disclaimer

All activities in this repository were performed in legal training environments and systems specifically provided for cybersecurity learning.

No real-world systems were targeted.
