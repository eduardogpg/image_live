import boto3

def upload_file(bucket, local_path, content_type, mediafile_key):
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
        print(err)
        return None

def show_objects(bucket):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        for object in bucket.objects.all():
            print(object)

    except Exception as err:
        print(err)
        return None

def create_folder(bucket, directory_name):
    try:
        s3 = boto3.client('s3')
        key = directory_name + '/'
        
        s3.put_object(Bucket=bucket, Key=key)
        return  key
    
    except Exception as err:
        print(err)
        return None
