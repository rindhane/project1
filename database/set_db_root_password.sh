#! /usr/bin/env bash
#make sure gcloud account is activated within the terminal
#read documentation for further customization and suppport 
#docs>>https://cloud.google.com/sql/docs/mysql/create-instance#gcloud

INSTANCE_NAME=;
PASSWORD=;

gcloud sql users set-password root \
--host=% \
--instance ${INSTANCE_NAME} \
--password ${PASSWORD}

