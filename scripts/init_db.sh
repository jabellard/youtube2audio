#!/bin/bash

# Script to initialize the database

# Named Arguments---------------------------------------------------
# -p : Root directory of the django project, defaults to './'

PROJECT_ROOT=''

while getopts ":p:" opt; do
  case $opt in
    p) PROJECT_ROOT="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$PROJECT_ROOT" ]
then
      PROJECT_ROOT=./
fi

init_db(){
  echo "Initializing database..."
  python ${PROJECT_ROOT}manage.py makemigrations &&
  python ${PROJECT_ROOT}manage.py migrate &&
  python ${PROJECT_ROOT}manage.py createsu &&
  python ${PROJECT_ROOT}manage.py loaddata sites.site.json &&
  echo "Done."
}

init_db
