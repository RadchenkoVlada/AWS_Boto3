# Upload file to bucket
## Input
* Bucket name
* uploaded file path (local)

## Output
Error or success

### Steps:
* Config loaded at start
* Validate the json file against the schema
* Path on the bucket is generated
* Upload to s3


# Download file to bucket

## Input
* Bucket name
* Downloaded file path (local)
* Parameters (Dict of strings) Example: {"city": "Rivne"}


## Output
Error or success

### Steps:
* Config loaded at start
* path on the bucket is generated



# Main flow

1. Create AWS S3 resource
2. Load all config files (in constructor)
   * if failed -> terminate program
   * Check schema files exists
3. Create 3 instances of our Service class
4call upload and download for each instance