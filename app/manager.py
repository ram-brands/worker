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

    def ensure_file_structure(self, ignored_paths, input_path):
        all_root_paths = set(os.listdir(self.root))
        root_paths = all_root_paths - set(ignored_paths)

        complete_input_path = self.get_path(input_path)

        if len(root_paths) == 1:
            (sole_path,) = root_paths
            complete_sole_path = self.get_path(sole_path)

            if os.path.isdir(complete_sole_path):
                os.rename(complete_sole_path, complete_input_path)
                return

        try:
            os.mkdir(complete_input_path)
        except FileExistsError:
            self.status = Status.CLIENT_ERROR

        for sub_path in root_paths:
            complete_old_path = self.get_path(sub_path)
            complete_new_path = os.path.join(complete_input_path, sub_path)

            try:
                os.rename(complete_old_path, complete_new_path)
            except OSError:
                self.status = Status.CLIENT_ERROR

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
