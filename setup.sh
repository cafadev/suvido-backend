#!/bin/bash

# Enable Git Hooks
cp pre-commit .git/hooks
cp pre-push .git/hooks

export_venv() {
    export PATH="/home/server/server/.venv/bin:$PATH"
    echo $PATH
}

django_access() {
    # Setup database, create admin user and enable github auth
    python manage.py migrate --no-input
    # python manage.py createfirstadmin
}

if [[ $ENV == "development" ]]; then
    # Install dependencies with pipenv
    pipenv install --dev
    export_venv
    django_access

    echo ""
    echo "********Container is ready********"
    echo ""
    # Keep running the container
    tail -f /dev/null
else
    pipenv install
    export_venv
    django_access
    # python manage.py collectstatic --no-input
    
    echo "Activating Gunicorn"
    # Start Daphne server
    gunicorn server.wsgi:application --bind 0.0.0.0:8080 --workers 4 --timeout 0 --max-requests 1000 --max-requests-jitter 50 --preload
fi
