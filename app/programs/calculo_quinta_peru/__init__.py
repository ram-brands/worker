import logging

from fs import FileSystem

from . import main

logger = logging.getLogger(__name__)


def exec(run_id):
    #########################
    # Mount the file system #
    #########################

    with FileSystem(run_id) as fs:
        main.run(fs)

        # path = "output/results.csv"
        # fs.makedirs(path)

        # with fs.open(path, mode="wb") as file:
        #     file.write(b"Hello, world!")

        # fs.commit_zip(dir="output")
