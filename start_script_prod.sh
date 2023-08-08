#! /bin/bash

# This script is used to start the application

cd backend
docker compose --env-file config/settings/.env.prof -f docker-compose.prod.yml up --build -d

cd ../frontend
npm install
npm start