import boto3

def upload_file(bucket, mediafile_key, file):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        return bucket.put_object(
            ACL='public-read',
            Key=mediafile_key,
            ContentType=file.content_type,
            Body=file,
        )
    
    except Exception as err:
        print(err)
        return None

def download_file(bucket, mediafile_key, local_path):
    try:
        s3 = boto3.client('s3')
        
        with open(local_path, 'wb') as f:
            s3.download_fileobj(bucket, mediafile_key, f)

        return True
        
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

def rename_file(bucket, new_mediafile_key, old_mediafile_key):
    try:
        
        s3 = boto3.resource('s3')
        
        s3.Object(bucket, new_mediafile_key).copy_from(CopySource=old_mediafile_key)
        s3.Object(bucket, old_mediafile_key).delete()

        return True
        
    except Exception as err:
        print(err)
        return None

def delete_mediafile(bucket, key):
    try:
    
        s3 = boto3.resource('s3')
        
        obj = s3.Object(bucket, key)
        obj.delete()

        return True
        
    except Exception as err:
        print(err)
        return None