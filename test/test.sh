#!/bin/bash

curl -i -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}' http://0.0.0.0:8000/api/user

curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/login
