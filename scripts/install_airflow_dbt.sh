#!/bin/bash
set -euo pipefail


AIRFLOW_HOME="$HOME/airflow"
PYTHON_VERSION="3.11"
AIRFLOW_VENV_PATH="$HOME/airflow_venv"
AIRFLOW_VERSION="2.10.5"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
DBT_HOME="$HOME/dbt"
DBT_VENV_PATH="$HOME/dbt_venv"
USER=$(whoami)
LOG_DIR="/var/log/airflow"

POSTGRES_USER="airflow"
POSTGRES_PASSWORD="airflow"
POSTGRES_DATABASE="airflow"


sudo apt-get update && sudo apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential libssl-dev libffi-dev python3-dev \
    postgresql postgresql-contrib libpq-dev

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DATABASE};"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DATABASE} TO ${POSTGRES_USER};"
sudo -u postgres psql -c "ALTER USER ${POSTGRES_USER} WITH SUPERUSER;"


python3 -m venv "${AIRFLOW_VENV_PATH}"
source "${AIRFLOW_VENV_PATH}/bin/activate"

sudo apt-get install -y --no-install-recommends \
    apt-utils ca-certificates curl dumb-init \
    freetds-bin krb5-user libgeos-dev ldap-utils libsasl2-2 \
    libsasl2-modules libxmlsec1 locales libffi8 libldap-2.5-0 libssl3 \
    netcat-openbsd lsb-release openssh-client python3-selinux rsync \
    sasl2-bin sqlite3 sudo unixodbc

pip install --upgrade pip
pip install --no-cache-dir \
    "apache-airflow[google,graphviz,mongo,postgres]==${AIRFLOW_VERSION}" \
    --constraint "${CONSTRAINT_URL}"

pip install --no-cache-dir \
    "apache-airflow-providers-google" \
    --constraint "${CONSTRAINT_URL}"

pip install scrapy
pip install psycopg2-binary

mkdir -p "${AIRFLOW_HOME}"/{dags,logs,plugins}

cat > "${AIRFLOW_HOME}/airflow.cfg" <<EOL
[core]
dags_folder = ${AIRFLOW_HOME}/dags
base_log_folder = ${AIRFLOW_HOME}/logs
executor = LocalExecutor
load_examples = False

[webserver]
web_server_host = 0.0.0.0
web_server_port = 8080
rbac = True

[database]
sql_alchemy_conn = postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost/${POSTGRES_DATABASE}
EOL

cd "${AIRFLOW_HOME}"
export AIRFLOW_HOME="${AIRFLOW_HOME}"
airflow db init


sudo mkdir -p "${LOG_DIR}"
sudo chown "${USER}":"${USER}" "${LOG_DIR}"



sudo tee /etc/systemd/system/airflow-webserver.service > /dev/null <<EOF
[Unit]
Description=Airflow Webserver
After=network.target postgresql.service

[Service]
User=${USER}
Group=${USER}
Type=simple
Environment="PATH=${AIRFLOW_VENV_PATH}/bin:/usr/local/bin:/usr/bin:/bin"
Environment="AIRFLOW_HOME=${AIRFLOW_HOME}"
ExecStart=${AIRFLOW_VENV_PATH}/bin/airflow webserver
WorkingDirectory=${AIRFLOW_HOME}
Restart=always
RestartSec=5
StandardOutput=append:${LOG_DIR}/webserver.log
StandardError=append:${LOG_DIR}/webserver.log

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/airflow-scheduler.service > /dev/null <<EOF
[Unit]
Description=Airflow Scheduler
After=network.target postgresql.service

[Service]
User=${USER}
Group=${USER}
Type=simple
Environment="PATH=${AIRFLOW_VENV_PATH}/bin:/usr/local/bin:/usr/bin:/bin"
Environment="AIRFLOW_HOME=${AIRFLOW_HOME}"
ExecStart=${AIRFLOW_VENV_PATH}/bin/airflow scheduler
WorkingDirectory=${AIRFLOW_HOME}
Restart=always
RestartSec=5
StandardOutput=append:${LOG_DIR}/scheduler.log
StandardError=append:${LOG_DIR}/scheduler.log

[Install]
WantedBy=multi-user.target
EOF


airflow users create \
    --username admin \
    --password "admin" \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

sudo systemctl daemon-reload
sudo systemctl enable airflow-webserver
sudo systemctl enable airflow-scheduler
sudo systemctl start airflow-webserver
sudo systemctl start airflow-scheduler

deactivate


python3 -m venv "${DBT_VENV_PATH}"
source "${DBT_VENV_PATH}/bin/activate"

pip install --upgrade pip
python3 -m pip install dbt-core dbt-bigquery


mkdir -p "${HOME}/.dbt"
cat > "${HOME}/.dbt/profiles.yml" <<EOL
default:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: your-gcp-project
      dataset: dbt_dev
      threads: 4
      timeout_seconds: 300
      location: asia-southeast1
EOL

deactivate
