#!/bin/sh

# Check if DJANGO_PORT is set, otherwise show an error and exit
: "${DJANGO_PORT:?error missing DJANGO_PORT env}"

# Function to wait for the Django service to be healthy
wait_for_django() {
    echo "Waiting for Django service on port $DJANGO_PORT..."
#    while ! nc -z web "$DJANGO_PORT"; do
    while ! curl -s "http://mti-app:$DJANGO_PORT" > /dev/null; do
        echo "Django service not ready, waiting..."
        sleep 5
    done
    echo "Django service is ready."
}

# Wait for Django before starting NGINX
wait_for_django

# Run NGINX and set up auto-reload every 6 hours
echo "Starting NGINX with auto-reload every 6 hours..."
(
    while :; do
        sleep 6h
        echo "Reloading NGINX..."
        nginx -s reload
    done
) &

# Start NGINX in the foreground
nginx -g 'daemon off;'