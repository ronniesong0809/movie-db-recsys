#!/bin/bash -x

PWD=`pwd`
echo $PWD
activate () {
  . $PWD/venv/bin/activate
}

install () {
  pip install -r requirements.txt
}

if [ ! -d "./venv" ]; then
  /usr/bin/virtualenv --python=python3 venv
  activate
  install
  deactivate venv
fi

if [ -d "./venv" ]; then
  activate
  python script.py
  python train.py
  python upload.py
  deactivate venv
fi
