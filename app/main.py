from fastapi import BackgroundTasks, FastAPI

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


@app.post("/", status_code=200)
async def index(run: Run, background_tasks: BackgroundTasks):
    program = programs[run.program_name]
    background_tasks.add_task(program.exec, run.run_id)
