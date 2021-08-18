#! /usr/bin/env bash

#docs support & directory
#https://cloud.google.com/sql/docs/mysql/create-manage-databases

DATABASE_NAME=;
INSTANCE_NAME=;

gcloud sql databases create ${DATABASE_NAME} \
        --instance=${INSTANCE_NAME} 
