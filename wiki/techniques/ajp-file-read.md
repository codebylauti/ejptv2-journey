---
type: technique
tags: [ejpt:web-pentest]
tools: []
cves: [CVE-2020-1938]
related: ["[[cve-2020-1938]]", "[[source-code-disclosure]]", "[[hiddencat]]"]
---

# AJP File Read

Reading files out of a Tomcat application through its **Apache JServ Protocol** connector (port 8009) — a channel HTTP fuzzing can never reach. This is the arbitrary-file-read half of [[cve-2020-1938]] (Ghostcat).

## What AJP is

AJP is the **binary protocol between a front-end web server (Apache httpd, nginx) and the Tomcat servlet container** — multiplexed and cheaper than proxying raw HTTP. Tomcat exposes it on a separate connector, `8009/tcp`, which nmap labels `ajp13 Apache Jserv (Protocol v1.3)`.

It is *meant* to be a loopback-only back channel: the front-end server speaks AJP, nobody else. On affected releases the connector **shipped enabled by default, bound to all interfaces**, and Tomcat grants AJP connections **higher trust than HTTP** — so anything you can send to 8009 is treated as a request from the trusted front-end. That trust gap is the whole primitive: the HTTP layer's refusal to serve `WEB-INF/*` simply doesn't apply on this port.

## Workflow

1. **Spot the tell** — `nmap -p-` shows **`8009/tcp open ajp13` next to an HTTP port running a named Tomcat version** ([[information-gathering]], [[nmap]]). An unusual protocol adjacent to a known product = look up CVEs for **both** the port and the version, not just the version.
2. **Run the PoC** — clone a public exploit (the vault used `Hancheng-Lei/Hacking-Vulnerability-CVE-2020-1938-Ghostcat`) and point it at the AJP port:

   ```sh
   python2 CVE-2020-1938.py <target> -p 8009 -f WEB-INF/web.xml
   ```

   `-p` = AJP port, `-f` = file path relative to the application root ([[cve-2020-1938]]).
3. **Read `WEB-INF/web.xml` first** — every Java web app has one, and it is the app's ID card: servlet names, init parameters, security constraints, and (as on [[hiddencat]]) a `<description>` that **names a user**. It is the highest-value first read because it turns "what is this app?" into "who is behind it?".
4. **Feed the loot onward** — a username from the descriptor goes straight into a brute-force ([[ssh-bruteforce]]); other paths (`WEB-INF/classes/*.properties`, source) seed follow-up reads ([[source-code-disclosure]]).

## Why it beats HTTP fuzzing

Files under `WEB-INF/` are **never served over HTTP** — the servlet specification forbids it, so no wordlist, traversal, or `curl` will fetch them. The AJP connector reads them anyway because it bypasses the HTTP layer entirely. When directory fuzzing returns nothing but Tomcat's default `docs/`/`examples/`/`manager/` redirects, the content isn't *behind a path* — it's behind a **different protocol** ([[directory-fuzzing]]). Changing the wordlist never finds it; changing the port does.

## Limits

- **Read demonstrated; RCE not.** [[cve-2020-1938]] also allows *processing* a file as a JSP (→ code execution), but that path needs content-control/upload conditions that vary per deployment. [[hiddencat]] exercised **only the file read** — treat inclusion/RCE as an environment-dependent bonus, not a given.
- **Reads are scoped by the Tomcat process's own access** — web-application files are the reliable target; system files (`/etc/passwd`-style) depend on exploit path and deployment.
- **It is not a shell.** Output is file contents; converting that into access (username → brute-force → login) is a separate, deliberate step.

## Seen in

[[hiddencat]] — `8009/ajp13` beside Tomcat 9.0.30 → Hancheng-Lei PoC → `WEB-INF/web.xml` `<description>` → **jerry** → hydra → `jerry:chocolate` → SUID python3.7 → root. Only `web.xml` was read.
