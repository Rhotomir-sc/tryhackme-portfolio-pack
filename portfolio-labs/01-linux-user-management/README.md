# 01 - Linux User Management

| Information | Details |
|---|---|
| Difficulty | Beginner |
| Category | Linux & Access Control |
| Platform | TryHackMe |
| Related Room | Linux Fundamentals Part 1 |
| Related Google Module | Linux & SQL |

---

## Overview

In this lab, I reviewed basic Linux user identity and account information in a temporary TryHackMe environment. I focused on understanding how a Linux system identifies users, stores account details, assigns groups, and protects sensitive authentication files.

The environment did not provide administrative access, so I worked with the existing account instead of creating or modifying users.

---

## Learning Goal

My goal was to understand the basic structure of a Linux user account and learn how user, group, home directory, and shell information can be reviewed from the terminal.

---

## What I Practiced

- Checking the currently logged-in user
- Reviewing UID, GID, and group membership
- Reading account information from `/etc/passwd`
- Reviewing user and group records with `getent`
- Checking the home directory and login shell
- Comparing the permissions of `/etc/passwd`, `/etc/group`, and `/etc/shadow`

---

## Google Cybersecurity Connection

I first reviewed basic Linux concepts in the Google Cybersecurity Certificate and then reinforced them through hands-on practice in this TryHackMe lab.

**Related Module:** Linux & SQL

---

## Command Notes

| Command | What I Used It For |
|---|---|
| `whoami` | Checked the currently logged-in user |
| `id` | Reviewed the user's UID, GID, and group membership |
| `groups` | Displayed the groups assigned to the current user |
| `getent passwd` | Reviewed account information such as the home directory and login shell |
| `getent group` | Checked the related group record |
| `ls -l` | Compared ownership and permissions of account-related files |

One detail I found important was that `/etc/passwd` and `/etc/group` were readable, while `/etc/shadow` had more restrictive permissions because it contains sensitive authentication information.

---

## Screenshots

### Current User and Identity

This output shows the current username, UID, GID, group membership, home directory, and login shell.

![Current user and identity](screenshots/01-current-user-and-identity.png)

### User Account Review

I reviewed account names from `/etc/passwd` and checked the UID, home directory, and shell information of standard users.

![User account review](screenshots/02-user-account-review.png)

### Account Files and Protection

I compared the ownership and permissions of `/etc/passwd`, `/etc/group`, and `/etc/shadow`.

![Account files and protection](screenshots/03-account-files-and-protection.png)

### User Environment Summary

This output provides a short summary of the active user's identity and environment.

![User environment summary](screenshots/04-user-environment-summary.png)

### Room Completion

The TryHackMe room was completed successfully.

![Linux Fundamentals Part 1 completed](screenshots/05-room-completed.png)

---

## Result

### What I Learned

I learned how Linux connects a username with a UID, primary group, home directory, and login shell. I also understood why account information and authentication data are stored with different permission levels.

### What I Found Most Useful

The comparison between `/etc/passwd` and `/etc/shadow` was the most useful part for me because it showed how Linux separates general account information from sensitive authentication data.

### Next Step

The next lab will focus on Linux file permissions, ownership, and the principle of least privilege.
