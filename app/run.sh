#!/bin/bash

if [ "$RUN_ENV" = "development" ]; then
  exec asymmetric run --host 0.0.0.0 --port $PORT asgi --reload --log-level debug
else
  exec asymmetric run --host 0.0.0.0 --port $PORT asgi --log-level info
fi
