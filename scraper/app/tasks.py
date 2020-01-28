import requests
import os
import re
import tarfile
from bs4 import BeautifulSoup
from app import celery, db
from app.models import TextContent, Image
from app.schema import UrlSchema
from definitions import ROOT_DIR, IMAGES_DIR_NAME


def parse_text_from_soup(soup):
    """
    Function used for cleaning text data from website and returning it in multiple lines format.
    :param soup: BeautifulSoup object containing parsed HTML
    :return: String with multiple lines, stripped of HTML tags etc., briefly cleaned up
    """
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)


def get_list_of_images(soup, url_object):
    """
    Function used to find all image paths in HTML soup, create links,
    and then return list of Image objects (refer to ORM models)
    :param soup: BeautifulSoup object containing parsed HTML
    :param url_object: deserialized Url object (refer to ORM models)
    :return: list of Image objects
    """
    list_of_images = []
    orm_list_of_images = []
    # searching for the images src
    for link in soup.find_all('img'):
        if link.get('src'):
            list_of_images.append(link.get('src'))
        elif link.get('data-src'):
            list_of_images.append(link.get('data-src'))
    for image in list_of_images:
        try:
            img_src, _, img_name = re.match(r"((.*)?\/(.*\.(?:png|jpg)))", image).groups()
            if img_src.startswith("http"):
                img_link = img_src
            elif img_src.startswith('//'):
                img_link = "https:" + img_src
            else:
                # joining url domain and img_src
                img_link = url_object.url.rsplit('/', 1)[0] + img_src

            # getting raw image and downloading it
            img_raw = requests.get(img_link, stream=True)
            with open(os.path.join(ROOT_DIR, IMAGES_DIR_NAME, url_object.name, img_name), 'wb') as file:
                for chunk in img_raw.iter_content(chunk_size=1024):
                    file.write(chunk)
                orm_list_of_images.append(Image(path=os.path.relpath(file.name, ROOT_DIR).encode("utf-8"), url=url_object))
        except AttributeError:
            # Upon finding wrong 'src' in the list_of_images, just skip it
            continue
    return orm_list_of_images


@celery.task
def get_data_from_url(url_serialized_object):
    """
    Celery task for saving data in the system and adding it to the database
    :param url_serialized_object: serialized Url object (refer to ORM models)
    :return: message "Task finished"
    """
    url_schema = UrlSchema()
    url_object = url_schema.load(url_serialized_object, session=db.session)
    soup = BeautifulSoup(requests.get(url_object.url).text, "html.parser")
    os.makedirs(os.path.join(ROOT_DIR, IMAGES_DIR_NAME, url_object.name), exist_ok=True)

    db.session.add(TextContent(text=parse_text_from_soup(soup).encode("utf-8"), url=url_object))
    db.session.add_all(get_list_of_images(soup, url_object))
    db.session.commit()

    tar_images.delay(url_object.name)
    return "Task finished"


@celery.task
def tar_images(name):
    """
    Celery task for creating an archive of all images saved in given 'name' directory
    :param name: name from the currently processed Url object
    :return: message that archive is created
    """
    tar_path = os.path.join(ROOT_DIR, IMAGES_DIR_NAME, f'{name}.tar')
    print(tar_path)
    with tarfile.open(os.path.join(IMAGES_DIR_NAME, f'{name}.tar'), 'w') as tar:
        tar.add(os.path.join(IMAGES_DIR_NAME, name))
    return f"Archive {name}.tar created"
