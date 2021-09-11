from manager import Manager

from . import main


def exec(run_id):
    with Manager(run_id) as _:
        main.run(_)
        _.output_dir = "results"
