---
type: platform
difficulties: [super-easy, easy, intermediate, hard]
related: [[tryhackme]]
---

# DockerLabs

Free Spanish platform of vulnerable Docker machines, great for building fundamentals.

## Completed boxes

### super-easy

- [[breakmyssh]] — SSH brute-force
- [[first-hacking]] — vsftpd 2.3.4 backdoor (CVE-2011-2523)
- [[hedgehog]] — web source leak → SSH brute-force → chained sudo
- [[trust]] — gobuster → hydra → sudo vim
- [[tproot]] — vsftpd 2.3.4 backdoor
- [[obsession]] — anonymous FTP + web hints → sudo vim
- [[vacaciones]] — HTML comment usernames → sudo ruby
- [[borazuwara]] — image metadata username → sudo group

### easy

- [[los-3-hackers]] — SQLi → session → cron → capabilities
- [[hannah-coffee]] — LFI + log poisoning → debugfs → capabilities
- [[balufood]] — leaked creds → secret_key reuse → .bashrc alias → root
- [[balulero]] — .env leak → sudo php → group-owned script → root
- [[nodeclimb]] — anon FTP → zip crack → sudo node writable script
- [[psycho]] — LFI → SSH key → chained sudo (perl → python3)
- [[autoescuela]] — Node.js Inspector RCE → React2Shell (CVE-2025-55182)
- [[wargames]] — prompt injection → hash crack → SUID binary

### intermediate

- [[adopting]] — web cache deception → writable /etc/passwd

### hard

- [[baluhome]] — XSS → cookie theft → Node reverse shell → cron abuse
