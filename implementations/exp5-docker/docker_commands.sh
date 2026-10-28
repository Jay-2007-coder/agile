#!/bin/bash
# ============================================================
# Experiment 5: Docker Commands Reference
# Run these commands in order to complete the experiment
# ============================================================

echo "=========================================="
echo "  Experiment 5: Docker Containerization"
echo "=========================================="

# -------------------------------------------------------
# STEP 1: Verify Docker Installation
# -------------------------------------------------------
echo ""
echo "STEP 1: Check Docker installation"
docker --version
docker info | head -10

# -------------------------------------------------------
# STEP 2: Build Docker Image
# -------------------------------------------------------
echo ""
echo "STEP 2: Build Docker image"
docker build -t online-book-store:1.0 .
docker build -t online-book-store:latest .

# List images
echo ""
echo "Available Docker images:"
docker images | grep online-book-store

# -------------------------------------------------------
# STEP 3: Run Container
# -------------------------------------------------------
echo ""
echo "STEP 3: Run container"
docker run -d \
    --name obs-container \
    -p 5000:5000 \
    -e FLASK_ENV=production \
    online-book-store:latest

# Check container is running
echo ""
echo "Running containers:"
docker ps

# -------------------------------------------------------
# STEP 4: Test the API
# -------------------------------------------------------
echo ""
echo "STEP 4: Test API endpoints"
sleep 3  # Wait for app to start

# Health check
echo "Health check:"
curl -s http://localhost:5000/health | python3 -m json.tool

# Get all books
echo ""
echo "Get all books:"
curl -s http://localhost:5000/books | python3 -m json.tool

# Search books
echo ""
echo "Search for 'java':"
curl -s "http://localhost:5000/books/search?q=java" | python3 -m json.tool

# Register user
echo ""
echo "Register user:"
curl -s -X POST http://localhost:5000/users/register \
     -H "Content-Type: application/json" \
     -d '{"username": "jay_student", "password": "password123"}' \
     | python3 -m json.tool

# Login
echo ""
echo "Login:"
curl -s -X POST http://localhost:5000/users/login \
     -H "Content-Type: application/json" \
     -d '{"username": "jay_student", "password": "password123"}' \
     | python3 -m json.tool

# Add a book
echo ""
echo "Add new book:"
curl -s -X POST http://localhost:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Flask Web Dev", "author": "Miguel Grinberg", "genre": "Python", "price": 700, "stock": 5}' \
     | python3 -m json.tool

# -------------------------------------------------------
# STEP 5: Container Logs
# -------------------------------------------------------
echo ""
echo "STEP 5: View container logs"
docker logs obs-container

# -------------------------------------------------------
# STEP 6: Inspect Container
# -------------------------------------------------------
echo ""
echo "STEP 6: Inspect container"
docker inspect obs-container | python3 -m json.tool | head -60

# -------------------------------------------------------
# STEP 7: Docker Compose (Multi-container)
# -------------------------------------------------------
echo ""
echo "STEP 7: Docker Compose"
docker-compose up -d
docker-compose ps
docker-compose logs

# -------------------------------------------------------
# STEP 8: Stop and Remove
# -------------------------------------------------------
echo ""
echo "STEP 8: Cleanup"
docker stop obs-container
docker rm obs-container
docker-compose down

echo ""
echo "Experiment 5 Complete!"
echo "Key Docker commands learned:"
echo "  docker build   - Build image from Dockerfile"
echo "  docker run     - Start a container"
echo "  docker ps      - List running containers"
echo "  docker logs    - View container logs"
echo "  docker inspect - Detailed container info"
echo "  docker stop    - Stop a container"
echo "  docker rm      - Remove a container"
echo "  docker-compose - Manage multi-container apps"
