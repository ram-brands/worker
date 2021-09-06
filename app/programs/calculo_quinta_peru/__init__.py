import logging

from fs import FileSystem
from .modules import reader

logger = logging.getLogger(__name__)


def exec(run_id):
    #########################
    # Mount the file system #
    #########################

    with FileSystem(run_id) as fs:

        ##############
        # Read files #
        ##############

        ####################
        # Process the data #
        ####################

        # Do stuff...

        ###############
        # Write files #
        ###############

        path = "output/results.csv"

        fs.makedirs(path)

        with fs.open(path, mode="wb") as file:
            file.write(b"Hello, world!")

        #####################
        # Commit the output #
        #####################

        # The files will be sent to the remote storage.
        fs.commit_zip(dir="output")

    # Upon exiting the context manager
    # the temporary file system will be destroyed.
