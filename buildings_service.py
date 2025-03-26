import json

from utilities import validate_json

from service import Service


class BuildingsService(Service):
    def __init__(self, bucket):
        super().__init__(bucket)

    def upload_file(self, upload_file_name):
        """
        Upload a file to an S3 bucket.
        :param upload_file_name: str, Name of the file to upload
        """
        if validate_json(upload_file_name, self.config["schema_file"]):
            with open(upload_file_name, 'r') as json_file:
                data = json.load(json_file)
            object_name_in_s3 = (data["country"]+'/'+ data["city"] + '/'+
                                 data["street_address"] + '/' + data["file_name"])
            self.upload_file_to_s3(upload_file_name, object_name_in_s3)
        else:
            raise Exception("Invalid JSON file")

    def download_file(self, download_file_name: str, parameters: dict[str,str]):
        """
        Download a file from an S3 bucket.

        :param download_file_name: Name of the file to download
        :param parameters: dict, location parameters for search in s3
        """
        #TODO: validate parameters
        required_keys = ["country", "city", "street_address", "file_name"]
        object_name_in_s3 = (parameters["country"] + '/' + parameters["city"] + '/' +
                             parameters["street_address"] + '/' + parameters["file_name"])
        self.download_file_from_s3(object_name_in_s3, download_file_name)


import json


def download_file(self, download_file_name: str, parameters: dict[str, str], schema_file_path: str):
    """
    Download a file from an S3 bucket after validating the parameters against a schema.

    :param download_file_name: Name of the file to download
    :param parameters: dict, location parameters for search in S3
    :param schema_file_path: Path to the JSON schema file
    """
    # Load schema from JSON file
    with open(schema_file_path, 'r') as schema_file:
        schema = json.load(schema_file)

    # Extract keys from schema
    schema_keys = schema.get("required", [])
    if not schema_keys:
        raise ValueError("Schema does not define required keys.")

    # Validate parameters
    missing_keys = [key for key in schema_keys if key not in parameters]
    extra_keys = [key for key in parameters if key not in schema_keys]

    if missing_keys:
        raise ValueError(f"Missing keys in parameters: {missing_keys}")
    if extra_keys:
        raise ValueError(f"Unexpected keys in parameters: {extra_keys}")

    # Construct S3 object name
    object_name_in_s3 = '/'.join([parameters[key] for key in schema_keys])
    self.download_file_from_s3(object_name_in_s3, download_file_name)
