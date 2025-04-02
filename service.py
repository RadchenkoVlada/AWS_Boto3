from multiprocessing.connection import Client

import boto3
import yaml
import sys
from pathlib import Path

from botocore.exceptions import ClientError

from constants import ROOT_DIR

from helpers.custom_logger import CustomLogger

class Service:
    def __init__(self, bucket: str):
        """
        Initialize the Service class with a config file.
        :param config_file: the path to configuration file

        Expects: a bucket name
        Modifies: Nothing
        Returns: object of 'Service' class
        """
        self.config_file = ROOT_DIR / "config.yaml"
        self.config = self._load_config(bucket)
        self._validate_schemas()
        self.s3 = boto3.resource('s3')
        self.logger = CustomLogger("Service logger", self.config)

    def _load_config(self, bucket: str) -> dict:
        """
        Load and parse the config file.

        Expects: a bucket name
        Modifies: Nothing
        Returns: Dictionary with bucket info. Keys could be like: bucket_name, schema_file, keys_for_file_structure...
        """
        if not Path(self.config_file).exists():

            raise FileExistsError(f"Configuration file '{self.config_file}' not found. Terminating program.")

        with open(self.config_file, 'r') as file:
            try:
                config = yaml.safe_load(file)
                print( config['buckets'][bucket])
                return config['buckets'][bucket]
            except yaml.YAMLError as e:
                print(f"Failed to parse configuration file: {e}. Terminating program.")
                sys.exit(1)


    def _validate_schemas(self) -> None:
        """
        Check if all schema files exist.

        Expects: No argument
        Modifies: Nothing
        Returns: None
        """
        schema_file = self.config.get("schema_file")
        if not schema_file or not (ROOT_DIR / schema_file).exists():
            self.logger.error(f"Schema file '{schema_file}' not found. Terminating program.")
            sys.exit(1)

    def all_buckets_in_s3(self) -> list:
        """
        Return a list of all bucket names in S3.

        Expects: No argument
        Modifies: Nothing
        Returns: List of bucket names
        """
        try:
            return [bucket.name for bucket in self.s3.buckets.all()]
        except Exception as e:
            self.logger.error(f"Error retrieving bucket list: {e}")
            return []

    def upload_file_to_s3(self, upload_file_name: str, object_name_in_s3=None) -> None:
        """
        Upload a file to an S3 bucket.

        :param upload_file_name: Name of the file to upload
        :param object_name_in_s3: Name to give the file in the bucket (optional)

        Expects: upload_file_name, object_name_in_s3
        Modifies: Nothing
        Returns: None
        """
        if object_name_in_s3 is None:
            object_name_in_s3 = upload_file_name

        if self.config['bucket_name'] in self.all_buckets_in_s3():
            self.s3.Bucket(self.config['bucket_name']).upload_file(upload_file_name, object_name_in_s3)
            self.logger.info(f"File {upload_file_name} was uploaded to {self.config['bucket_name']} as {object_name_in_s3}")
        else:
            raise Exception(f"Bucket {self.config['bucket_name']} does not exist")

    def download_file_from_s3(self, download_file_name: str, download_path: str) -> None:
        """
        Download a file from an S3 bucket.

        :param download_file_name: Name of the file to download
        :param download_path: Path where the downloaded file will be saved

        Expects: download_file_name, download_path
        Modifies: Nothing
        Returns: None
        """
        if self.config['bucket_name'] in self.all_buckets_in_s3():
            try:
                self.s3.Object(self.config['bucket_name'], download_file_name).load()
                self.logger.debug("Object exists.")
                print("Object exists.")
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    raise FileNotFoundError(f"The object '{download_file_name}' does not exist.")
            # downloads the specified object
            self.s3.Bucket(self.config['bucket_name']).download_file(download_file_name, download_path)
            self.logger.info(f"File \"{download_file_name}\"was downloaded from \"{self.config['bucket_name']}\" and saved as {download_path}")
        else:
            raise Exception(f"Bucket {self.config['bucket_name']} does not exist")
