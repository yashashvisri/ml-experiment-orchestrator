#!/bin/bash
# Deployment script for EC2 / Ubuntu servers

echo "🚀 Starting Production Deployment..."

# 1. Pull latest code
echo "📦 Pulling latest changes from git..."
git pull origin main

# 2. Rebuild and restart docker containers
echo "🐳 Rebuilding Docker containers..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

echo "✅ Deployment complete! The AI Orchestrator is now live."
