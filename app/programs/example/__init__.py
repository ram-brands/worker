import logging

from fs import FileSystem

logger = logging.getLogger(__name__)


def exec(run_id):
    with FileSystem(run_id) as fs:

        ########################
        # Mount the filesystem #
        ########################

        fs.mount()

        ##############
        # Read files #
        ##############

        with fs.open("some_folder/data.xls", mode="rb") as file:
            some_more_data = file.read()

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
        # The temporary file system will be destroyed.
        fs.commit_zip(dir="output")
