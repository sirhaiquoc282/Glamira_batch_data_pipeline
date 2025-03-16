#!/bin/bash

source dbt-env/bin/activate
cd glamira_dbt
dbt run

deactivate