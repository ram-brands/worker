from fastapi import FastAPI

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

import env
from programs import programs

app = FastAPI()

sentry_sdk.init(dsn=env.SENTRY_DSN, environment=env.FASTAPI_ENV)

app.add_middleware(SentryAsgiMiddleware)


@app.post("/")
def index(program_name: str, run_id: str):
    program = programs[program_name]
    program.exec(run_id)
    return "OK"
