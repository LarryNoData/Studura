#!/bin/bash
flask db upgrade
exec gunicorn app:app
