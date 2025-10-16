

Ở đây ứng dụng là Fancy Store gồm 2 phần:

1. **Frontend:** giao diện React hiển thị sản phẩm, đơn hàng.
2. **Backend:** chứa 2 microservices — Orders và Products (Node.js).

Hai phần này được triển khai trên hai VM riêng biệt:
- Một VM gắn **tag `frontend`**, chạy React.
- Một VM gắn **tag `backend`**, chạy Node.js API.

Bước 1: Tạo một Cloud Storage Bucket
```
gsutil mb gs://fancy-store-Project ID
```

Bước 2: git clone
```
https://github.com/googlecodelabs/monolith-to-microservices.git
```




```
#!/bin/bash

# Install logging monitor. The monitor will automatically pick up logs sent to
# syslog.
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

# Install dependencies from apt
apt-get update
apt-get install -yq ca-certificates git build-essential supervisor psmisc

# Install nodejs
mkdir /opt/nodejs
curl https://nodejs.org/dist/v16.14.0/node-v16.14.0-linux-x64.tar.gz | tar xvzf - -C /opt/nodejs --strip-components=1
ln -s /opt/nodejs/bin/node /usr/bin/node
ln -s /opt/nodejs/bin/npm /usr/bin/npm

# Get the application source code from the Google Cloud Storage bucket.
mkdir /fancy-store
gsutil -m cp -r gs://fancy-store-[DEVSHELL_PROJECT_ID]/monolith-to-microservices/microservices/* /fancy-store/

# Install app dependencies.
cd /fancy-store/
npm install

# Create a nodeapp user. The application will run as this user.
useradd -m -d /home/nodeapp nodeapp
chown -R nodeapp:nodeapp /opt/app

# Configure supervisor to run the node app.
cat >/etc/supervisor/conf.d/node-app.conf << EOF
[program:nodeapp]
directory=/fancy-store
command=npm start
autostart=true
autorestart=true
user=nodeapp
environment=HOME="/home/nodeapp",USER="nodeapp",NODE_ENV="production"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update
```




```
gcloud compute instances create backend \
    --zone=us-west1-a \
    --machine-type=e2-standard-2 \
    --tags=backend \
   --metadata=startup-script-url=https://storage.googleapis.com/fancy-store-qwiklabs-gcp-02-88d68d00ee82/startup-script.sh
```