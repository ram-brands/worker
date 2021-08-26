import os
from pathlib import Path

############
# ENV VARS #
############

FASTAPI_ENV = os.environ.get("RUN_ENV")

SENTRY_DSN = os.environ.get("SENTRY_DSN")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_REGION = os.environ.get("AWS_REGION")
RUNS_S3_BUCKET = os.environ.get("RUNS_S3_BUCKET")

AWS_LOCATION = os.environ.get("AWS_LOCATION", "")


###################
# LOCAL OVERWRITE #
###################

LOCAL_STEM = "local"
LOCAL_PATH = Path(f"env/{LOCAL_STEM}.py")

if LOCAL_PATH.exists():
    from .local import *  # noqa: F401,F403
