# Project3: Linux Server Configurtion

This project is about hosting your item catalog project on the web by installing Linux distribution- ubuntu on the VM and configuring web/database servers in a secure manner to protect it from number of attack vectors.

## Table of Contents
- [Required Info](#Required-info)
- [Amazon Lightsail set-up](#Amazon-Lightsail-set-up)
- [Terminal time-zone and port config](#Terminal-time-zone-and-port-config)
- [Install Software packages](#Install-Software-packages)
- [Create grader's account](#Create-grader's-account)
- [Deploy Item Catalog project to the server](#Deploy-Item-Catalog-project-to-the-server)
- [Third-party Resources](#third-party-resources)

### Required Info
Public IP Address: 52.90.161.249<br/>
SSH Port: 2200<br/>
App URL: http://ec2-52-90-161-249.compute-1.amazonaws.com<br/>
Graders login info: ssh -v -i ~/.ssh/udacity_key.pem grader@52.90.161.249 -p 2200

### Amazon Lightsail set-up
1. Follow the `Get started on Lightsail` document available on Udacity
2. Go to your instance and download the private key and rename it to udacity_key.pem
3. Then move the key to ~/.ssh directory
4. Then go to the `Network` tab and add custom ports:<br/>
    (i) Custom UDP 123 <br/>
    (ii) Custom TCP 2200

### Terminal time-zone and port config
Change to your local time: `sudo dpkg-reconfigure tzdata`<br/>
Firewall port config:
1. sudo ufw allow 2200/tcp
2. sudo ufw allow 80/tcp
3. sudo ufw allow 123/upd
4. sudo ufw enable

### Install Software packages
Log into your VM and install all the following needed packages:
1. sudo apt-get update
2. sudo apt-get upgrade
3. sudo apt-get install finger
4. sudo apt-get install ntp
5. sudo apt-get install apache2
6. sudo apt-get install libapache2-mod-wsgi python-dev
7. sudo apt-get install git
8. sudo pip install Flask
9. sudo pip install flask_oauth
10. sudo pip install httplib2
11. sudo pip install oauth2client
12. sudo pip install sqlalchemy
13. sudo pip install psycopg2
14. sudo pip install sqlalchemy_utils
14. sudo apt-get install libpq-dev python-dev
15. sudo apt-get install postgresql postgresql-contrib
16. sudo apt-get install python-pip
17. sudo pip install virtualenv

### Create grader's account
1. log into your root account: ssh -i ~/.ssh/udacity_key.pem ubuntu@`public ip`
2. Create new user: `sudo adduser grader`
3. open the config dile `sudo nano /etc/sudoers.d/grader` and add:
<br/><t/>(i) grader ALL=(ALL:ALL) ALL <br/>
4. Open file: `sudo nano /etc/hosts`and add:
<br/><t/>(i) 127.0.1.1 ip-public <br/>
5. SSH grader's login:<br/>
```
sudo mkdir /home/grader/.ssh
sudo touch /home/grader/.ssh/authorized_keys
sudo cp /root/.ssh/authorized_keys /home/grader/.ssh/authorized_keys
sudo chmod 700 /home/grader/.ssh
sudo chmod 644 /home/grader/.ssh/authorized_keys
```
6. Grader's root ownership:<br/>
```
sudo chown -R grader:grader /home/grader/.ssh
sudo service ssh restart
```

7. Cofigure port:2200<br/>
  `sudo nano /etc/ssh/sshd_config` and replace port 22 with 2200
8. Remove root login :<br/>
`sudo nano /etc/ssh/sshd_config` and set PermitRootLogin  to No

### Deploy Item Catalog project to the server
1. log into the graders account
2. start apache and wsgi:<br/> `sudo a2enmod wsgi`<br/>
`sudo service apache2 start`<br/>
3. set up the git:<br/>
```
git config --global user.name
git config --global user.email
sudo cd /var/www
sudo mkdir catalog
sudo cd catalog
sudo git clone [project url] catalog
```
4. wsgi configuration:<br/>
 `sudo cd /var/www/catalog`<br/>`sudo nano catalog.wsgi`

5. add the following to catalog.wsgi:<br/>
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/")
from catalog import app as application
application.secret_key = 'anyphrase'
```
6. Configure virtul env and rename your app to `__init__.py`<br/>
```
sudo cd /var/www/catalog/catalog
sudo mv application.py __init__.py
sudo virtualenv venv
source venv/bin/activate
```

7. go to the catalog config file: `sudo nano /etc/apache2/sites-available/catalog.conf` and add the following:
```
<VirtualHost *:80>
   ServerName public.ip
   ServerAlias hostname.amazonaws.com
   ServerAdmin admin@public.ip
   WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
   WSGIProcessGroup catalog
   WSGIScriptAlias / /var/www/catalog/catalog.wsgi
   <Directory /var/www/catalog/catalog/>
       Order allow,deny
       Allow from all
   </Directory>
   Alias /static /var/www/catalog/catalog/static
   <Directory /var/www/catalog/catalog/static/>
       Order allow,deny
       Allow from all
   </Directory>
   ErrorLog ${APACHE_LOG_DIR}/error.log
   LogLevel warn
   CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
8. Restart the server:
```
sudo service apache2 reload
sudo a2ensite catalog
```
9. configure the database:
```
sudo su - postgres
psql
CREATE USER catalog WITH PASSWORD 'password';
ALTER USER catalog CREATEDB;
CREATE DATABASE catalog with OWNER catalog;
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;
\q
exit
```

10. In files: animeApp.py, database_anime.py, and database_setup.py:<br/>
Find: `engine = create_engine('sqlite:///catalog.db')`<br/>
Replace: `engine = create_engine('postgresql://catalog:password@localhost/catalog')`

11. Update the `console.developers.google.com` API urls

### Third-party Resources
https://github.com/jessica-hsu/Full-stack-Nanodegree/tree/master/project7<br/>
https://github.com/chuanqin3/udacity-linux-configuration<br/>
https://github.com/SruthiV/Linux-Server-Configuration
