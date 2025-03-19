#!/bin/bash
set -euo pipefail

MONGO_VERSION="8.0"
ADMIN_USER="admin"
ADMIN_PASSWORD="admin"
MONGO_PORT="27017"

sudo apt-get install -y gnupg curl


curl -fsSL https://www.mongodb.org/static/pgp/server-${MONGO_VERSION}.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg


echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/${MONGO_VERSION} multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-${MONGO_VERSION}.list

sudo apt-get update
sudo apt-get install -y mongodb-org

cat <<EOF | sudo tee /etc/mongod.conf
net:
  port: $MONGO_PORT
  bindIp: 0.0.0.0

security:
  authorization: enabled
EOF

sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl start mongod

sleep 10

mongosh --port $MONGO_PORT admin <<EOF
db.createUser({
  user: "$ADMIN_USER",
  pwd: "$ADMIN_PASSWORD",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})
EOF

echo "MongoDB setup completed successfully!"
