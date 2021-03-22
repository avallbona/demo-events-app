#!/bin/bash

set -e

case $1 in
    run-devel)
        /entrypoint.sh launch-migrations
        python manage.py runserver 0.0.0.0:8000
        ;;
    launch-migrations)
        echo "→ Executing migrate"
        exec python manage.py migrate
        echo "✓ Migrations applied"
        ;;
    launch-tests)
        echo "→ Executing tests"
        exec pytest
        echo "✓ Executed tests"
        ;;
    *)
        exec "$@"
        ;;
esac
