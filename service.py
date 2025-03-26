from multiprocessing.connection import Client

import boto3
import yaml
import sys
from pathlib import Path

from botocore.exceptions import ClientError

from constants import ROOT_DIR

class Service:
    def __init__(self, bucket: str):
        """
        Initialize the Service class with a config file.
        :param config_file: path to configuration file
        """
        self.config_file = ROOT_DIR / "config.yaml"
        self.config = self._load_config(bucket)
        self._validate_schemas()
        self.s3 = boto3.resource('s3')

    def _load_config(self, bucket):
        """Load and parse the config file."""
        if not Path(self.config_file).exists():

            raise FileExistsError(f"Configuration file '{self.config_file}' not found. Terminating program.")

        with open(self.config_file, 'r') as file:
            try:
                config = yaml.safe_load(file)
                return config['buckets'][bucket]
            except yaml.YAMLError as e:
                print(f"Failed to parse configuration file: {e}. Terminating program.")
                sys.exit(1)


    def _validate_schemas(self):
        """
        Check if all schema files exist.
        """
        schema_file = self.config.get("schema_file")
        if not schema_file or not (ROOT_DIR / schema_file).exists():
            print(f"Schema file '{schema_file}' not found. Terminating program.")
            sys.exit(1)

    def all_buckets_in_s3(self) -> list:
        """
        Return a list of all bucket names in S3.

        :return: List of bucket names
        """
        try:
            return [bucket.name for bucket in self.s3.buckets.all()]
        except Exception as e:
            print(f"Error retrieving bucket list: {e}")
            return []

    def upload_file_to_s3(self, upload_file_name: str, object_name_in_s3=None):
        """
        Upload a file to an S3 bucket.

        :param upload_file_name: Name of the file to upload
        :param object_name_in_s3: Name to give the file in the bucket (optional)
        """
        if object_name_in_s3 is None:
            object_name_in_s3 = upload_file_name

        if self.config['bucket_name'] in self.all_buckets_in_s3():
            self.s3.Bucket(self.config['bucket_name']).upload_file(upload_file_name, object_name_in_s3)
            # TODO: rewrite all prints to logger
            print(f"File {upload_file_name} was uploaded to {self.config['bucket_name']} as {object_name_in_s3}")
        else:
            raise Exception(f"Bucket {self.config['bucket_name']} does not exist")

    def download_file_from_s3(self, download_file_name: str, download_path: str):
        """
        Download a file from an S3 bucket.

        :param download_file_name: Name of the file to download
        :param download_path: Path where the downloaded file will be saved
        """
        if self.config['bucket_name'] in self.all_buckets_in_s3():
            # checks if the specified object (download_file_name) exists in the specified bucket (bucket_name).
            try:
                self.s3.Object(self.config['bucket_name'], download_file_name).load()
                print("Object exists.")
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    raise FileNotFoundError(f"The object '{download_file_name}' does not exist.")
            # downloads the specified object
            self.s3.Bucket(self.config['bucket_name']).download_file(download_file_name, download_path)
            print(f"File \"{download_file_name}\"was downloaded from \"{self.config['bucket_name']}\" and saved as {download_path}")
        else:
            raise Exception(f"Bucket {self.config['bucket_name']} does not exist")
