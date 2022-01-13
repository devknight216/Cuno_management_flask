FROM nginx:1.21.4

RUN apt update
RUN apt upgrade -y && \
    apt install -y wget tar xz-utils htop systemctl vim 

# Python installation, from https://www.linuxcapable.com/how-to-install-python-3-8-on-debian-11-bullseye/
RUN cd /tmp && \
    wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz

RUN cd /tmp && tar -xf Python-3.8.12.tar.xz -C /tmp
RUN cd /tmp && ls -la && \
    mv Python-3.8.12 /opt/Python3.8.12

RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

# TODO: change to --enable-optimizations but that's slower build
RUN cd /opt/Python3.8.12 && \
    ./configure --enable-shared && \
    make -j `nproc` && \
    make altinstall && \
    ldconfig /opt/Python3.8.12

# removed:  python3.8-dev python3-distutils python3-pip python3.8-venv
RUN apt install -y uwsgi uwsgi-src uuid-dev libcap-dev libpcre3-dev

# Copy in the Python app
RUN mkdir -p /var/www/myapp/
COPY myapp /var/www/myapp/

# Setting up a uWSGI Python 3.8 app:

RUN cd /tmp && \
    export PYTHON=python3.8 && \
    uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python38" && \
    mv python38_plugin.so /usr/lib/uwsgi/plugins/python38_plugin.so && \
    chmod 666 /usr/lib/uwsgi/plugins/python38_plugin.so

SHELL ["/bin/bash", "-c"]

RUN cd /var/www/myapp && \
    python3.8 -m venv myenv && \
    source myenv/bin/activate && \
    python3 -m pip install -r requirements.txt

# setting up the nginx server to pass through to uwsgi
RUN mkdir -p /etc/nginx/sites-available/ && \
    mkdir -p /etc/nginx/sites-enabled/
COPY myapp.conf /etc/nginx/sites-available/myapp.conf
COPY myapp.ini /var/www/myapp/myapp.ini
# this is needed to start the uwsgi service but even without it I see a uwsgi service
COPY myapp.service /etc/systemd/system/myapp.service
RUN ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/myapp.conf

# Temporarily not using the myapp.ini file because can't get NGINX to communicate through the unix socket
COPY start_uwsgi_webserver.sh /var/www/myapp/start_uwsgi_webserver.sh
RUN chmod +rwx /var/www/myapp/start_uwsgi_webserver.sh

RUN systemctl enable myapp
