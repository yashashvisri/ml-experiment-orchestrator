# Production Deployment Guide

This guide explains how to deploy the AI Experiment Orchestrator to a production server (like AWS EC2, DigitalOcean Droplet, etc.) using Docker.

## Prerequisites
1. A Linux server (Ubuntu recommended)
2. Docker and Docker Compose installed
3. Git installed

## 1. Clone the Repository
SSH into your server and clone the code:
```bash
git clone https://github.com/yashashvisri/ml-experiment-orchestrator.git
cd ml-experiment-orchestrator
```

## 2. Setup Environment Variables
Copy the production environment template:
```bash
cp .env.prod.example .env
```
Edit `.env` using `nano .env` and securely fill in:
- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `GEMINI_API_KEY`

## 3. Deploy
Make the deployment script executable and run it:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 4. Access the Application
The Streamlit Frontend is exposed on port `80`. You can access it by typing your server's public IP address directly into your browser!

The FastAPI Backend is exposed on port `8000`.
