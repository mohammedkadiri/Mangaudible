
from google.cloud import storage

storage_client = storage.Client()

def retrieve_url(bucket_name, manga_name, chapter, page_no):
    img_url = "Invalid manga name"
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
       if manga_name in blob.name:
           img_url = "https://storage.cloud.google.com/{}/manga/{}/{}/{}.jpg".format(bucket_name, manga_name, chapter, page_no)
    return img_url

def page_count(bucket_name, manga_name, chapter):
    blobs = storage_client.list_blobs(bucket_name)
    count = 0
    for blob in blobs:
        if manga_name in blob.name:
            if chapter in blob.name:
                count +=1
    return count
          