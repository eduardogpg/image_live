import boto3

def upload_image(bucket, local_path, content_type, mediafile_key):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        return bucket.put_object(
            ACL='public-read',
            Body=open(local_path, 'rb'),
            ContentType=content_type,
            Key=mediafile_key
        )
    
    except Exception as err:
        print('Error s3')
        print(err)
        return None
