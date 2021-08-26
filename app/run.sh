#!/bin/bash

if [ "$RUN_ENV" = "development" ]; then
  exec uvicorn main:app --host 0.0.0.0 --port $PORT --reload --log-level debug
else
  exec uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info
fi
