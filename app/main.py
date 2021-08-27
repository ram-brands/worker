from fastapi import FastAPI

import sentry_sdk
from pydantic import BaseModel
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

import env
from programs import programs

app = FastAPI()

sentry_sdk.init(dsn=env.SENTRY_DSN, environment=env.FASTAPI_ENV)

app.add_middleware(SentryAsgiMiddleware)


class Run(BaseModel):
    program_name: str
    run_id: str


@app.post("/")
def index(run: Run):
    program = programs[run.program_name]
    program.exec(run.run_id)
    return "OK"
