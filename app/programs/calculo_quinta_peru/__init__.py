from fs import FileSystem

from . import main


def exec(run_id):
    with FileSystem(run_id) as fs:
        import time

        time.sleep(30)

        main.run(fs)
        fs.commit_zip(dir="results")
