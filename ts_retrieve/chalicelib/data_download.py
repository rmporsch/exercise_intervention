import boto3
import botocore
from pydantic import BaseSettings
import logging
import os
from typing import List


class Settings(BaseSettings):
    bucket: str = "example-project-aia"
    region: str = "asia-southeast-1"
    files: List[str] = [
        "dailyActivity_summary.csv",
        "dailySleep_summary.csv",
        "dailyWeightLog_summary.csv",
        "hourlyActivity_summary.csv",
        "weightLog-report.csv"
    ]


class S3(object):

    def __init__(self, settings: Settings):
        self._settings = settings
        self._s3 = boto3.resource('s3')

    def download(self, destination: str):
        try:
            for file in self._settings.files:
                output = os.path.join(destination, file)
                self._s3.Bucket(self._settings.bucket).download_file(file, output)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def upload(self, files: List[str]):
        try:
            for f in files:
                self._s3.upload_file(f, self._settings.bucket, f)
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            return False
        return True
