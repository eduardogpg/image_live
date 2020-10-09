import boto3

def upload_file(bucket, mediafile_key, file):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        return bucket.put_object(
            ACL='public-read',
            Key=mediafile_key,
            ContentType=file.content_type,
            Body=file,#open(local_path, 'rb'),
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
