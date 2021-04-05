from google.cloud import storage, exceptions

storage_client = storage.Client()

def retrieve_url(bucket_name, manga_name, chapter, page_no):
    '''
    Fetches the image url of a manga page stored within the bucket
    E.g. retrieve_url("mangaudible", "Grand Blue", "chapter1", 1)
    https://storage.cloud.google.com/mangaudible/manga/Grand Blue/chapter1/1.jpg

    :bucket_name: Bucket name on google cloud storage 
    :manga_name : Manga name stored inside the bucket
    :chapter: Chapter to retrieve
    :page_no: Page number to retrieve
    '''
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
    '''
    Returns the total number of pages within a manga chapter
    E.g page_count("mangaudible", "Grand Blue", "chapter1") = 50
    :bucket_name: Bucket name on google cloud storage 
    :manga_name : Manga name stored inside the bucket
    :chapter: Chapter to retrieve
    '''
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


# print(page_count("mangaudible", "Grand Blue", "chapter1"))
   
          
