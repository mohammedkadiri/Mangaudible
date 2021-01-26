from bs4 import BeautifulSoup
import requests
import os


def scraper(path, manga_titles, chapters):
    '''
    Scrapes a manga page from the given urls.

    It scrapes all the manga provided from the manga page urls and the number of
    chapters to scrape.


    :param path: A list containing the paths to retrieve a specific manga where grand-blue represents the path -
    https://rawdevart.com/comic/grand-blue
    :param manga_titles: List of manga titles corresponding to each path
    :param chapters: Number of chapters to retrieve
    :return: Key pair of manga and list of manga img_urls
    '''
    index = 0
    manga = {}
    for name in manga_titles:
        img_urls = []
        for manga_chapter in range(1, chapters):
            page = 'https://rawdevart.com/comic/{0}/chapter-{1}/'.format(path[index], manga_chapter)
            response = requests.get(page, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == requests.codes.ok:
                page_content = BeautifulSoup(response.text, 'lxml')
                for img in page_content.find_all('img', class_='img-fluid not-lazy'):
                    img_urls.append(img['data-src'])
        index += 1
        manga[name] = img_urls
    return manga


def create_folders(filepath, manga_titles):
    '''
    Create folders in filepath.

    :param filepath: filepath to create folders
    :return: None
    '''
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
    except OSError as error:
        print("Directory cannot be created")
    else:
        for title in manga_titles:
            full_path = "{0}{1}".format(filepath, title)
            chapter1_path = "{0}{1}/chapter1".format(filepath, title)
            chapter2_path = "{0}{1}/chapter2".format(filepath, title)
            os.makedirs(full_path)
            os.makedirs(chapter1_path)
            os.makedirs(chapter2_path)


def download_manga(manga):
    '''
    Downloads and stores each manga page.

    :param manga: key,pair containing a list of image urls for each manga key
    :return: None
    '''
    for key in manga.keys():
        print(key)
        page = 1
        for url in manga[key]:
            filename = "C:/Users/Manga/{0}/{1}.jpg".format(key, page)
            file_stream = requests.get(url, stream=True)
            with open(filename, 'wb') as f:
                for data in file_stream:
                    f.write(data)
            page += 1
        print("Download complete")


with open('../../Documents/Project/Mangaudible/mangas.txt') as f:
    path = [line.rstrip('\n') for line in f]

with open('../../Documents/Project/Mangaudible/titles.txt') as f:
    manga_titles = [line.rstrip('\n') for line in f]

chapters = 3
filepath = "C:/Users/manga/"

manga = scraper(path, manga_titles, chapters)
print(manga)
# create_folders(filepath, manga_titles)
# download_manga(manga)
