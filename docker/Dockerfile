FROM ubuntu:16.04
LABEL author="abderrazak.zidane@d2-si.eu" version="1.0"

# Utils installation
ENV DEBIAN_FRONTEND noninteractive
ENV EDITOR vim
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y vim sudo

# Postgresql installation
RUN apt-get install -y postgresql postgresql-contrib

# Create myd2si user with password myd2si
RUN adduser --gecos "" -disabled-password myd2si
RUN ["/bin/bash", "-c", "echo -e 'myd2si\nmyd2si' | passwd myd2si"]

# add myd2si user to sudoers
COPY sudoers /etc/sudoers

# Jump to postgres user
USER postgres

# restart the service, add a new postgres role, create new db
RUN ["/bin/bash", "-c", "service postgresql restart && echo -e 'myd2si\nmyd2si' | createuser myd2si && createdb myd2si"]

# force password for database access
COPY pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf

#Jump to root user
USER root

# install firewall ubuntu and git andnginx
RUN apt-get install -y ufw git nginx
RUN apt-get install -y python3-pip python3-dev libpq-dev

# set up firewall ubuntu
#TODO: RUN ufw enable && ufw allow 'Nginx HTTP' && ufw allow ssh

# create nginx config
COPY myd2si-api-rest.conf /etc/nginx/sites-available/myd2si-api-rest.conf

# activate the config
RUN ln -s /etc/nginx/sites-available/myd2si-api-rest.conf /etc/nginx/sites-enabled/

# create project directory
RUN mkdir /var/www/html/myd2si-api-rest
RUN sudo chown myd2si:myd2si /var/www/html/myd2si-api-rest

RUN pip3 install virtualenv

# jump to myd2si user + git clone
USER myd2si
RUN ["/bin/bash",  "-c", \
    "cd /var/www/html/myd2si-api-rest && \
    git clone https://github.com/rezid/api-rest.git . && \
    mkdir log && \
    virtualenv venv --python=python3.5 && \
    source venv/bin/activate && pip install -r requirements.txt"]


# start nginx
#RUN service nginx restart