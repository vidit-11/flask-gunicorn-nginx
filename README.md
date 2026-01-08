# flask-gunicorn-nginx
This repository contains a simple Flask application and a comprehensive guide for deploying it on a Linux server (Ubuntu/Debian) using Gunicorn as the application server and Nginx as the reverse proxy.

---

### Step 1: Server & User Setup
Create a dedicated user and configure SSH access.

```bash
sudo adduser deployuser
sudo usermod -aG sudo deployuser
# Edit sshd_config if you need password login
sudo nano /etc/ssh/sshd_config # Set PasswordAuthentication yes
sudo systemctl restart sshd

```

### Step 2: Clone & Environment Setup

```bash
git clone <link> <app_folder_name>
cd <app_folder_name>
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

```

### Step 3: Configure Systemd (Automatic Start)

Create a service file at `/etc/systemd/system/<app_name>.service`:

```ini
[Unit]
Description=Gunicorn instance to serve peak Flask app
After=network.target

[Service]
User=<user>
Group=www-data
WorkingDirectory=/home/<user>/<app_folder_name>
Environment="PATH=/home/<user>/<app_folder_name>/env/bin"
ExecStart=/home/<user>/<app_folder_name>/env/bin/gunicorn --workers 3 --bind unix:<app_name>.sock -m 007 wsgi:<app_name>

[Install]
WantedBy=multi-user.target

```

**Enable the service:**

```bash
sudo systemctl daemon-reload
sudo systemctl start <app_name>
sudo systemctl enable <app_name>

```

### Step 4: Configure Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/<conf_file>`:

```nginx
server {
    listen 80;
    server_name YOUR_IP_OR_DOMAIN;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/<user>/<app_folder_name>/<app_name>.sock;
    }
}

```

**Activate Nginx:**

```bash
sudo ln -s /etc/nginx/sites-available/<app_name> /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

```

##  Troubleshooting

* **Logs:** `sudo tail -f /var/log/nginx/error.log`
* **Permissions:** If 502 error occurs, run `sudo chmod 755 /home/<user>`
