from pprint import pprint
import requests
import os
import time
from tqdm import tqdm

mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in tqdm(mylist):
    time.sleep(1)

vk_token = ''


def create_local_directory():
    path = 'images'
    os.mkdir(path)


def get_photo(owner_id, directory):
    url_vk = 'https://api.vk.com/method/photos.get'
    params_vk = {
        'access_token': vk_token,
        'album_id': 'wall',
        'extended': 1,
        'v': '5.131'
    }
    img = requests.get(url=url_vk, params=params_vk).json()
    res_vk = img['response']['items']
    for el in res_vk:
        image_name = str(el['likes']['count'])
        info = {}
        info.setdefault(image_name, el['sizes'][9]['url'])
        for k, v in info.items():
            file_name = k + '.jpg'
            img_data = requests.get(el['sizes'][9]['url']).content
            with open(f'{directory}/{file_name}', 'wb') as file:
                file.write(img_data)
    return


ya_token = ""


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(url=upload_url, headers=headers, params=params)
        return response.json()

    def create_directory(self, dir_name: str):
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + ya_token
        }
        params = {
            'path': dir_name
        }
        r = requests.put(url=url, params=params, headers=headers)
        res = r.json()

    def upload_files_to_disk(self, disk_file_path, file_name):
        self.create_directory('Photo_vk')
        href = self._get_upload_link(disk_file_path=disk_file_path).get('href', '')
        response = requests.put(url=href, data=open(file_name, 'rb'))
        if response.status_code == 201:
            pprint('Success')
        else:
            pprint('False')


if __name__ == '__main__':
    create_local_directory()
    get_photo(310885834, 'images')
    ya = YaUploader(token=ya_token)
    ya.upload_files_to_disk('Photo_vk/26.jpg', 'images/26.jpg')
    ya.upload_files_to_disk('Photo_vk/29.jpg', 'images/29.jpg')
    ya.upload_files_to_disk('Photo_vk/6.jpg', 'images/6.jpg')
    ya.upload_files_to_disk('Photo_vk/34.jpg', 'images/34.jpg')
