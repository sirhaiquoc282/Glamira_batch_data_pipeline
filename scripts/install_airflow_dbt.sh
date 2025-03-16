#!/bin/bash
set -euo pipefail

AIRFLOW_HOME="$HOME/airflow"
PYTHON_VERSION="3.11"
AIRFLOW_VENV_PATH="$HOME/aiflow_venv"
AIRFLOW_VERSION="2.10.5"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
DBT_HOME="$HOME/dbt"
DBT_VENV_PATH="$HOME/dbt_venv"
USER=$(whoami)  


sudo apt-get update && sudo apt-get install -y \
    python3 python3-pip python3-venv 


python3 -m venv ${AIRFLOW_VENV_PATH}
source ${AIRFLOW_VENV_PATH}/bin/activate

sudo apt install -y --no-install-recommends  apt-utils ca-certificates curl dumb-init \
    freetds-bin krb5-user libgeos-dev ldap-utils libsasl2-2 \
    libsasl2-modules libxmlsec1 locales libffi8 libldap-2.5-0 libssl3 \
    netcat-openbsd lsb-release openssh-client python3-selinux rsync \
    sasl2-bin sqlite3 sudo unixodbc


pip install --no-cache-dir \
    "apache-airflow[google,graphviz,mongo]==${AIRFLOW_VERSION}" \
    --constraint "${CONSTRAINT_URL}"

pip install --no-cache-dir \
    "apache-airflow-providers-google" \
    --constraint "${CONSTRAINT_URL}"

pip insatll scrapy

mkdir -p ${AIRFLOW_HOME}/{dags,logs,plugins}

cd ${AIRFLOW_HOME}

airflow db init

sudo mkdir -p /var/log/airflow
sudo chown $USER:$USER /var/log/airflow


sudo tee /etc/systemd/system/airflow-webserver.service > /dev/null <<EOF
[Unit]
Description=Airflow Webserver
After=network.target

[Service]
User=$USER
Group=$USER
Environment="PATH=$AIRFLOW_VENV_PATH/airflow/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$AIRFLOW_VENV_PATH/airflow/bin/airflow webserver
WorkingDirectory=/home/nguyenhaiquoc282/airflow
Restart=always
RestartSec=5
StandardOutput=append:/var/log/airflow/webserver.log
StandardError=append:/var/log/airflow/webserver.log

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/airflow-scheduler.service > /dev/null <<EOF
[Unit]
Description=Airflow Scheduler
After=network.target

[Service]
User=$USER
Group=$USER
Environment="PATH=$AIRFLOW_VENV_PATH/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$AIRFLOW_VENV_PATH/bin/airflow scheduler
WorkingDirectory=$HOME/airflow
Restart=always
RestartSec=5
StandardOutput=append:/var/log/airflow/scheduler.log
StandardError=append:/var/log/airflow/scheduler.log

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

python3 -m venv ${DBT_VENV_PATH}
source ${DBT_VENV_PATH}/bin/activate


python3 -m pip install dbt-core dbt-bigquery

deactivate


