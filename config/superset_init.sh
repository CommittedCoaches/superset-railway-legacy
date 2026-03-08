#!/bin/bash

# create Admin user, you can read these values from env or anywhere else possible
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"

# Upgrading Superset metastore
superset db upgrade

# setup roles and permissions
superset superset init

# Create read-only public viewer account for anonymous dashboard embeds
superset fab create-user --username public_viewer --firstname Public --lastname Viewer --email public@localhost --password "$(openssl rand -hex 32)" --role Gamma || true

# Starting server
/bin/sh -c /usr/bin/run-server.sh