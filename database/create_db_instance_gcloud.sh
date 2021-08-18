#! /usr/bin/env bash
#make sure gcloud account is activated within the terminal
#read documentation for further customization and suppport 
#docs>>https://cloud.google.com/sql/docs/mysql/create-instance#gcloud


myinstance=write-instanace-name;

gcloud sql instances create ${myinstance} \
--database-version=MYSQL_8_0 \
--cpu=2 \
--memory=7680MB \
--region=asia-south1
