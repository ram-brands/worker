import time

from manager import Manager

from status import Status


def exec(run_id):
    ##########################
    # Initialize the manager #
    ##########################

    with Manager(run_id) as _:
        _.ensure_file_structure(
            input_path="input", ignored_paths=[".DS_Store", "__MACOSX"]
        )

        ##############
        # Read files #
        ##############

        with open(_.get_path("input/some_folder/data.xls"), mode="rb") as file:
            some_data = file.read()

        ####################
        # Process the data #
        ####################

        # Do stuff...
        time.sleep(5)

        # Log stuff...
        _.log("Example log.")
        _.warning("Example warning.")

        ###############
        # Write files #
        ###############

        path = "output/results.csv"

        _.makedirs(path)

        with open(_.get_path(path), mode="wb") as file:
            file.write(b"Hello, world!")

        #####################
        # Commit the output #
        #####################

        # The files will be saved to the remote storage.
        _.output_dir = "output"

        ##################
        # Set the status #
        ##################

        _.status = Status.WARNING

    # Upon exiting the context manager
    # the temporary file system will be destroyed.
