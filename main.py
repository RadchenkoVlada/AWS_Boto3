from buildings_service import BuildingsService
from constants import UPLOAD_FOLDER, DOWNLOAD_FOLDER

if __name__ == '__main__':
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
        # Uploading
        # upload_file_name = UPLOAD_FOLDER / 's3_buildings/kharkiv_info_26_032025.json.json'
        # building_service_object1 = BuildingsService(bucket='buildings')
        # building_service_object1.upload_file(upload_file_name)



        #Downloading
        parameters = {
            "country": "Ukraine",
            "city": "Kharkiv",
            "street_address": "Sumska Street",
            "file_name": "kharkiv_info_26_032025.json",
        }
        download_file_path = DOWNLOAD_FOLDER / 's3_buildings/kharkiv_info_26_032025.json'
        building_service_object1 = BuildingsService(bucket='buildings')
        building_service_object1.download_file(download_file_path, parameters=parameters)

        building_service_object1.logger.add_divider()


    except Exception as e:
        print(f"Error occurred: {e}")
        raise


