import boto3

def upload_image(bucket, local_path, mediafile_key):
    try:
        s3 = boto3.client('s3')
        return s3.upload_file(local_path, bucket, mediafile_key)

    except Exception as err:
        print('Error s3')
        return None
