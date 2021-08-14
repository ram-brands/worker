import logging
import os
import shutil
from io import BytesIO
from zipfile import ZipFile

from storage import Storage

logger = logging.getLogger(__name__)

TMP_DIR = lambda dir: os.path.join(".", "tmp", dir)


class FileSystem:
    def __init__(self, run_id):
        self.run_id = run_id
        self.root = TMP_DIR(dir=run_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroys the temporary file system.
        """
        shutil.rmtree(self.root)

    def mount(self):
        """
        Mounts the contents of the input to the temporary file system.
        """
        file = Storage().open(path=f"{self.run_id}/input.zip")

        content = file.read()
        buffer = BytesIO(content)
        zipfile = ZipFile(buffer)

        root = TMP_DIR(dir=self.run_id)
        zipfile.extractall(root)

    def makedirs(self, path):
        complete_path = os.path.join(self.root, path)

        dir = os.path.dirname(complete_path)
        os.makedirs(dir, exist_ok=True)

    def commit_zip(self, dir):
        """
        Commits the contents of the output to the remote storage.
        """
        buffer = BytesIO()
        commit_dir = os.path.join(self.root, dir)

        with ZipFile(file=buffer, mode="w") as zipfile:
            for dir, _, paths in os.walk(commit_dir):
                for path in paths:
                    complete_path = os.path.join(dir, path)
                    base = os.path.basename(path)
                    logger.info(complete_path)
                    zipfile.write(filename=complete_path, arcname=base)

        buffer.seek(0)
        return Storage().save(path=f"{self.run_id}/output.zip", file=buffer)

    @property
    def open(self):
        class FileContextManger:
            def __init__(obj, path, **kwargs):
                root = TMP_DIR(dir=self.run_id)
                complete_path = os.path.join(root, path)
                obj.file = open(complete_path, **kwargs)

            def __enter__(obj):
                return obj.file

            def __exit__(obj, exc_type, exc_value, traceback):
                obj.file.close()

        return FileContextManger
