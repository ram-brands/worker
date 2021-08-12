import boto3
from botocore.client import Config as BotoConfig

import env


class Storage:
    bucket_name = env.RUNS_S3_BUCKET

    def __init__(self):
        self.client = boto3.client(
            service_name="s3",
            region_name=env.AWS_REGION,
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            config=BotoConfig(signature_version="s3v4"),
        )

    @staticmethod
    def get_key(path):
        return env.AWS_LOCATION + path

    @staticmethod
    def validate_response(response):
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        response_is_ok = 200 <= status_code < 300
        if not response_is_ok:
            raise Exception(f"Remote storage responded with status code {status_code}")

    def open(self, path):
        response = self.client.get_object(Bucket=self.bucket_name, Key=self.get_key(path))
        self.validate_response(response)
        return response["Body"]

    def save(self, path, file):
        content = file.read()
        response = self.client.put_object(
            Bucket=self.bucket_name, Key=self.get_key(path), Body=content
        )
        self.validate_response(response)
