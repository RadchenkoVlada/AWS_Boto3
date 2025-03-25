import boto3
from botocore.exceptions import ClientError
from service import Service
from buildings_service import BuildingsService

if __name__ == '__main__':
    # print(all_buckets_in_s3())
    # print(list(s3.buckets.all()))

    # Upload
    # bucket_name = 's3-storage-classes-demo-2025-3month'
    # bucket_name = 's3-storage-classes-2025-3month-buildings'

    # upload_file_name = 'uploaded_files/nested_data_20_03.json'
    # object_name_in_s3 = 'ua/kharkiv/nested_data_20_03.json'
    #
    # print(upload_file_to_s3(bucket_name, upload_file_name, object_name_in_s3))

    # Download
    # bucket_name = 's3-storage-classes-demo-2025-3month'
    #
    # # download_file_name = "coffeee.jpg"
    # # download_file_name = "coffeeee.jpg"
    # # download_path = r'download_files\download_coffee3.jpg'
    # # print(download_file_from_s3(bucket_name, download_file_name, download_path))
    #
    # download_file_name = "ua/kharkiv/nested_data_18_03.json"
    # download_path = r'download_files\19_03_2025.json'
    # print(download_file_from_s3(bucket_name, download_file_name, download_path))
    try:
        # upload_file_name = 'uploaded_files/nested_data_20_03.json'
        # object_name_in_s3 = 'ua/kharkiv/nested_data_20_03.json'
        # building_service = Service(config_file='configs/config_buildings.yaml')
        # building_service.upload_file_to_s3(upload_file_name, object_name_in_s3)
        upload_file_name = 'uploaded_files/s3_buildings/kharkiv1_info.json'
        # TODO: pathlib
        building_service_object1 = BuildingsService(bucket='buildings')
        building_service_object1.upload_file(upload_file_name)

        copy_file_name = 'uploaded_files/s3_buildings/kharkiv1_info_copy.json'
        building_service_object1.download_file(copy_file_name, {
            "country": "Ukraine",
            "city": "Kharkiv",
            "street_address": "Galaya Street",
            "file_name": "kharkiv1_info.json",
        })

        # download_file_name = 'Ukraine/Kharkiv/street1/kharkiv1_info.json'
        # download_path = r'download_files/s3_buildings/kharkiv1_info_downloaded.json'
        # building_service_object1.download_file_from_s3(download_file_name, download_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

# https://aws-vlada-v1.signin.aws.amazon.com/console
