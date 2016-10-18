#!/bin/bash

gunicorn --reload -b localhost:8080 application.wsgi:application
