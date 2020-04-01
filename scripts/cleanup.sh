#!/usr/bin/env bash

# Export environment variables
source ../.env

# Drop and create database
mysql -u ${DB_USER} -p${DB_PASSWORD} -h ${DB_HOST} -e "DROP DATABASE ${DB_NAME};\
CREATE DATABASE ${DB_NAME} CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci; "

cd ..
pwd

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate
