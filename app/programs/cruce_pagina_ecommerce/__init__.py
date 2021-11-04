from manager import Manager

from . import main


def exec(run_id):
    with Manager(run_id) as _:
        _.ensure_file_structure(
            ignored_paths=[".DS_Store", "__MACOSX"], input_path="data"
        )
        main.run(_)
        _.output_dir = "results"
