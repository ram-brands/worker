from fastapi import FastAPI

# import env
from programs import example

# import sentry_sdk
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


app = FastAPI()

# sentry_sdk.init(dsn=env.SENTRY_DSN, environment=env.FASTAPI_ENV)

# asgi_app = SentryAsgiMiddleware(app)


programs = dict(example=example)


@app.post("/")
def index(program_name: str, run_id: str):
    program = programs[program_name]
    program.exec(run_id)
    return "OK"
