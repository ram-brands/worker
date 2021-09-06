import logging

from fs import FileSystem

from . import main

logger = logging.getLogger(__name__)


def exec(run_id):
    with FileSystem(run_id) as fs:
        main.run(fs)
        fs.commit_zip(dir="results")
