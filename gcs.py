from google.cloud import storage

storage_client = storage.Client()

def retrieve_url(bucket_name, manga_name, chapter, page_no):
    
    img_url = "Invalid manga name"

    blobs = storage_client.list_blobs(bucket_name)
    
    for blob in blobs:
       if manga_name in blob.name:
           img_url = "https://storage.cloud.google.com/{}/manga/{}/{}/{}.jpg".format(bucket_name, manga_name, chapter, page_no)
    return img_url
           
           
url = retrieve_url("mangaudible", "Koroshi Ai", "chapter2", "5")
print(url)