#!/bin/bash

# Build and run the Docker containers in detached mode
docker-compose up --build -d

# Wait for the web service to be healthy (optional, but good practice)
echo "Waiting for web service to be ready..."
until docker-compose exec web python -c "import django; print('Django is ready')" &> /dev/null; do
  sleep 5
done

# Apply database migrations
docker-compose exec web python manage.py migrate

echo "Docker setup complete. Access the application at http://localhost:8000/"
