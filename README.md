# AWS Python Services
The main idea of Service class and its subclasses is to create an abstraction for AWS s3 file storage.
Users of Services are not aware of AWS buckets details including folders hierarchy, files.
### Features
* upload
* download

## Upload file to bucket
### Input
* Bucket name
* uploaded file path (local)

### Output
Error or success

### Steps:
* Config loaded at start
* Validate the json file against the schema
* Path on the bucket is generated
* Upload to s3


## Download file from bucket

### Input
* Bucket name
* Downloaded file path (local)
* Parameters (Dict of strings)
   * parameters are set of values which obtained externally, for example by UI or API
   * parameters are used to find the file in the bucket
   * if parameters are invalid -> raises Exception
   * Example: `parameters = {
            "country": "Ukraine",
            "city": "Kharkiv",
            "street_address": "Sumska Street",
            "file_name": "kharkiv_info_26_032025.json",
        }`


### Output
Error or success

### Steps:
* Config loaded at start
* validate parameters
* path on the bucket is generated
* download from s3

# Main flow

1. Create AWS S3 resource
2. Load config files (in constructor)
   * if failed -> terminate program
   * Check schema files exists
3. Create 3 instances of our Service class
4. Call upload and download for each instance