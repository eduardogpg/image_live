import boto3

def upload_file(bucket, mediafile_key, content_type, local_path):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        return bucket.put_object(
            ACL='public-read',
            Key=mediafile_key,
            ContentType=content_type,
            Body=open(local_path, 'rb'),
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
