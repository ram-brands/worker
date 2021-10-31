import logging
import os
import shutil
from io import BytesIO, StringIO
from zipfile import ZipFile

import requests

import env
from status import Status
from storage import Storage

logger = logging.getLogger(__name__)

TMP_DIR = lambda dir: os.path.join(".", "tmp", dir)


class Manager:
    def __init__(self, run_id):
        self.run_id = run_id
        self.root = TMP_DIR(dir=run_id)

        self.storage = Storage()
        self.mount()

        self.logs_string = ""
        self.warnings_string = ""

        self.status = Status.OK
        self.output_dir = "output"

    @property
    def input_path(self):
        return f"{self.run_id}/input.zip"

    @property
    def output_path(self):
        return f"{self.run_id}/output.zip"

    @property
    def logs_path(self):
        return f"{self.run_id}/logs.txt"

    @property
    def warnings_path(self):
        return f"{self.run_id}/warnings.txt"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroys the temporary file system,
        saves the logs and warnings files,
        and confirms the transaction to the web server.
        """
        if exc_type:
            self.status = Status.SERVER_ERROR

        try:
            self.commit_output()
            shutil.rmtree(self.root)

            self.commit_logs()
            self.commit_warnings()

        except Exception as e:
            self.status = Status.SERVER_ERROR
            raise Exception(e) from e

        finally:
            confimation_url = f"{env.BACKEND_URL}/runs/{self.run_id}/confirmation"
            requests.post(url=confimation_url, json=dict(status=self.status.value))

    def ensure_file_structure(self):
        root_paths = os.listdir(self.root)
        new_base = self.get_path("data")

        if len(root_paths) == 1:
            old_base = self.get_base(root_paths[0])

            if os.base.isdir(old_base):
                os.rename(old_base, new_base)

                return

        try:
            os.mkdir(new_base)

        except FileExistsError as e:
            self.status = Status.CLIENT_ERROR
            raise Exception(e) from e

        for path in root_paths:
            old_path = os.path.join(self.root, path)
            new_path = os.path.join(new_base, old_path)

            os.rename(old_path, new_path)

    def mount(self):
        """
        Mounts the contents of the input to the temporary file system.
        """
        file = Storage().open(path=self.input_path)
        content = file.read()

        # Unzip files into root directory
        buffer = BytesIO(content)
        zipfile = ZipFile(buffer)
        zipfile.extractall(self.root)

        self.ensure_file_structure()

    def get_path(self, subpath):
        return os.path.join(self.root, subpath)

    def makedirs(self, path):
        complete_path = self.get_path(path)
        dir = os.path.dirname(complete_path)
        os.makedirs(dir, exist_ok=True)

    def log(self, msg, file=True, stdout=True):
        if file:
            self.logs_string += f"{msg}\n"

        if stdout:
            logger.info(msg)

    def warning(self, msg, file=True, stdout=True):
        if file:
            self.warnings_string += f"{msg}\n"

        if stdout:
            logger.info(msg)

    def commit_output(self):
        """
        Commits the contents of the output to the remote storage.
        """
        buffer = BytesIO()
        commit_dir = os.path.join(self.root, self.output_dir)

        with ZipFile(file=buffer, mode="w") as zipfile:
            for dir, _, paths in os.walk(commit_dir):
                for path in paths:
                    complete_path = os.path.join(dir, path)
                    relative_path = os.path.relpath(complete_path, self.root)

                    zipfile.write(filename=complete_path, arcname=relative_path)

        buffer.seek(0)
        return self.storage.save(path=self.output_path, file=buffer)

    def commit_logs(self):
        logs_buffer = StringIO(self.logs_string)
        self.storage.save(path=self.logs_path, file=logs_buffer)

    def commit_warnings(self):
        warnings_buffer = StringIO(self.warnings_string)
        self.storage.save(path=self.warnings_path, file=warnings_buffer)
