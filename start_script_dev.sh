#! /bin/bash

# This script is used to start the application

cd backend
docker compose --env-file config/settings/.env.dev up --build -d

cd ../frontend
npm install
npm start