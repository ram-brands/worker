from asymmetric import asymmetric as app

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

import env
from programs import example

sentry_sdk.init(dsn=env.SENTRY_DSN, environment=env.STARLETTE_ENV)

# asgi_app = SentryAsgiMiddleware(app)


programs = dict(example=example)

@app.router("/", methods=["post"])
def index(program_name, run_id):
    program = programs[program_name]
    program.exec(run_id)
    return "OK"
