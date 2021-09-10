from fs import FileSystem

from . import main


def exec(run_id):
    with FileSystem(run_id) as fs:
        main.run(fs)
        fs.commit_zip(dir="results")
