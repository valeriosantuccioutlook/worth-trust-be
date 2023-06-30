#!/bin/bash

echo "SETTING ENV..."
# Create .env file
touch .env

# Populate .env with non-sensitive vars
source devenv.txt; echo "ENVIRON="$ENVIRON >> .env
source devenv.txt; echo "DB_USER="$DB_USER >> .env
source devenv.txt; echo "DB_NAME="$DB_NAME >> .env
source devenv.txt; echo "DB_PORT="$DB_PORT >> .env
source devenv.txt; echo "DB_HOST="$DB_HOST >> .env
source devenv.txt; echo "EMAIL_HOST="$EMAIL_HOST >> .env
source devenv.txt; echo "EMAIL_PORT="$EMAIL_PORT >> .env
source devenv.txt; echo "EMAIL_FROM="$EMAIL_FROM >> .env

# Populate .env with ensitive vars stored in Github secrets
echo "ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES >> .env
echo "ALGORITHM="$ALGORITHM >> .env
echo "DB_PSW="$DB_PSW >> .env
echo "EMAIL_PASSWORD="$EMAIL_PASSWORD >> .env
echo "EMAIL_USERNAME="$EMAIL_USERNAME >> .env
echo "SECRET_KEY="$SECRET_KEY >> .env

echo "DONE"