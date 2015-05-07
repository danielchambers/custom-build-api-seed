#!/bin/bash

# install web server dependencies
sudo apt-get update
sudo apt-get -y install python python-virtualenv nginx supervisor

# install application (source location in $1)
mkdir /home/vagrant/bmw
cp $1/requirements.txt /home/vagrant
cp -R $1/bmw/* /home/vagrant/bmw/

# create a virtualenv and install dependencies
virtualenv /home/vagrant/bmw/venv
source /home/vagrant/bmw/venv/bin/activate
sudo /home/vagrant/bmw/venv/bin/pip install -r /home/vagrant/requirements.txt

# configure supervisor
sudo cp /vagrant/bmw.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/bmw
sudo supervisorctl reread
sudo supervisorctl update

# configure nginx
sudo cp /vagrant/bmw.nginx /etc/nginx/sites-available/bmw
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/bmw /etc/nginx/sites-enabled/
sudo service nginx restart

echo Application deployed to http://localhost:5000/