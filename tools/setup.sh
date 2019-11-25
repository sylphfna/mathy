#!/bin/bash
set -e
echo "Setting up all apps..."
libraries="mathy_python website"
for library in $libraries
do
   echo "=== Setting up: $library"
   (cd libraries/$library && sh tools/setup.sh)
done


# Make the virtualenv only if the folder doesn't exist
echo "Installing root virtualenv (.env)"
DIR=.env
if [ ! -d "${DIR}" ]; then
  virtualenv .env -p python3.6
fi

. .env/bin/activate
echo "Installing/updating requirements..."
pip install -e ./libraries/mathy_python
