def generate_configuration(custom_name, domain, working_directory, gunicorn_location, db_name=None, db_user=None,
                           db_password=None, celery=None):
    # Additional configurations
    additional_config = f"""
            sudo apt update
            sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
            
            sudo -u postgres psql
            
            CREATE DATABASE {db_name};
            CREATE USER {db_user} WITH PASSWORD '{db_password}';
            
            ALTER ROLE {db_user} SET client_encoding TO 'utf8';
            ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';
            ALTER ROLE {db_user} SET timezone TO 'UTC';
            
            GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};
            """
                # Base configurations
    base_config = f"""\
            /var/projects/{custom_name}/env
            /var/projects/{custom_name}/{custom_name}
            
            python manage.py migrate
            python manage.py collectstatic
            python manage.py createsuperuser
            pip install gunicorn
            
            sudo nano /etc/systemd/system/{custom_name}.socket
            
            [Unit]
            Description=gunicorn socket
            
            [Socket]
            ListenStream=/run/{custom_name}.sock
            
            [Install]
            WantedBy=sockets.target
            
            
            sudo nano /etc/systemd/system/{custom_name}.service
            
            
            [Unit]
            Description=gunicorn daemon
            Requires={custom_name}.socket
            After=network.target
            
            [Service]
            User=root
            Group=www-data
            WorkingDirectory={working_directory}
            ExecStart={gunicorn_location} \\
                      --access-logfile - \\
                      --workers 4 \\
                      --bind unix:/run/{custom_name}.sock \\
                      {custom_name}.wsgi:application
            
            [Install]
            WantedBy=multi-user.target
            
            
            sudo systemctl start {custom_name}.socket
            sudo systemctl enable {custom_name}.socket
            sudo systemctl status {custom_name}.socket
            
            file /run/{custom_name}.sock
            sudo journalctl -u {custom_name}.socket
            curl --unix-socket /run/{custom_name}.sock localhost
            sudo journalctl -u {custom_name}
            
            sudo systemctl daemon-reload
            sudo systemctl restart {custom_name}
            
            sudo nano /etc/nginx/sites-available/{domain}
            
            
            server {{
                listen 80;
                server_name {domain};
            
                location = /favicon.ico {{ access_log off; log_not_found off; }}
                location /static/ {{
                    root {working_directory};
                }}
            
                location / {{
                    include proxy_params;
                    proxy_pass http://unix:/run/{custom_name}.sock;
                }}
            }}
            
            
            
            sudo ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled
            sudo nginx -t
            sudo systemctl restart nginx
            journalctl -xeu nginx.service
            
            
            
            
            
            #certbot
            
            sudo apt install certbot python3-certbot-nginx
            sudo nano /etc/nginx/sites-available/{domain}
            sudo nginx -t
            sudo systemctl reload nginx
            sudo certbot --nginx -d {domain}
            sudo python3.10 /usr/local/bin/certbot --nginx -d {domain}
            sudo certbot --nginx -d {domain} --rsa-key-size 2048
            sudo certbot --nginx -d {domain} --rsa-key-size 2048
            
            sudo systemctl status certbot.timer
            sudo certbot renew --dry-run
            
            
            
            sudo nano /etc/systemd/system/{custom_name}_beat.service
            
            [Unit]
            Description=Celery {custom_name} Beat Scheduler
            After=network.target
            
            [Service]
            Type=simple
            WorkingDirectory={working_directory}
            ExecStart=/bin/bash -c '/var/projects/{custom_name}/env/bin/celery -A {custom_name} beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler'
            Restart=always
            User=root
            
            [Install]
            WantedBy=multi-user.target
            
            
            
            
            
            sudo nano /etc/systemd/system/{custom_name}_worker.service
            
            [Unit]
            Description=Celery {custom_name} Worker
            After=network.target
            
            [Service]
            Type=simple
            WorkingDirectory={working_directory}
            ExecStart=/bin/bash -c '/var/projects/{custom_name}/env/bin/celery -A {custom_name} worker  -Q {custom_name}_queue --loglevel=info '
            Restart=always
            User=root
            
            [Install]
            WantedBy=multi-user.target
            

            celery -A  {celery} beat --loglevel=info  --scheduler django_celery_beat.schedulers:DatabaseScheduler
            celery -A  {celery} worker  --loglevel=info
            """

    config = base_config
    if db_name and db_user and db_password:
        config = additional_config + base_config

    with open(f'{custom_name}_setup.txt', 'w') as file:
        file.write(config)


project_name=input("Enter project name: ")
domain=input("Enter domain: ")
working_directory=input("Enter working directory: ")
gunicorn_location=input("Enter gunicorn location: ")
db=input("Do you want to add database? (y/n): ")
if db=="y":
    db_name=input("Enter database name: ")
    db_user=input("Enter database user: ")
    db_password=input("Enter database password: ")

celery=input("Do you want to add celery? (y/n): ")
if celery=="y":
    celery_queue=input("Enter celery : ")


