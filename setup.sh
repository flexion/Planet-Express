#!/bin/bash

APP_ROOT="PlanetExpress/settings"

# setup virtual env
echo "Setting up virtual environment (env)"
virtualenv --no-site-packages env
echo "Activating virtual environment"
source env/bin/activate

# install dependencies
pip install -r requirements.txt

if [ ! -f "$APP_ROOT/local_settings.py" ]; then
    echo "
Copying default local settings
"
    cp "$APP_ROOT/local_settings-template.py" "$APP_ROOT/local_settings.py"
fi

