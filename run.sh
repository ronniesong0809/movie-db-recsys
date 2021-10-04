#!/bin/bash -x

PWD=`pwd`
activate () {
  . $PWD/venv/bin/activate
}

logging () {
  read -p "Logging? (y/n): " confirm2 && [[ $confirm2 == [yY] ]] || gunicorn app:app
  if echo "$confirm2" | grep -iq "^y" ;then
    gunicorn --error-logfile=- --access-logfile=- app:app
  fi
}

debugmode () {
  read -p "Debug Mode? (y/n): " confirm1 && [[ $confirm1 == [yY] ]] || logging
  if echo "$confirm1" | grep -iq "^y" ;then
    python3 app.py
  fi
}

if [ -d "./venv" ]; then
  activate
  debugmode
  deactivate venv
fi