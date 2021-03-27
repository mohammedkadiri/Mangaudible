from google.cloud import storage, exceptions

storage_client = storage.Client()

def retrieve_url(bucket_name, manga_name, chapter, page_no):
    img_url = "Invalid manga name"
    try: 
        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            if manga_name in blob.name:
                img_url = "https://storage.cloud.google.com/{}/manga/{}/{}/{}.jpg".format(bucket_name, manga_name, chapter, page_no)
    except exceptions.NotFound:
        print("ERROR: GCS bucket not found, path={}".format(bucket_name))
    finally:
        return img_url


def page_count(bucket_name, manga_name, chapter):
    count = 0
    try:
        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            if manga_name in blob.name:
                if chapter in blob.name:
                    count +=1
    except exceptions.NotFound:
        print("ERROR: GCS bucket not found, path={}".format(bucket_name)) 
    return count
   
          
