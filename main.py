from pprint import pprint
import requests
import os


vk_token = 'b3d3d411825d34f278bc76f7af9bb94365635ddb41fff1fe491fc09fd67066713f55047909035263ee408'


def get_photo(owner_id):
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
            with open(file_name, 'wb') as file:
                file.write(img_data)
    return


ya_token = "AQAAAABZrWRJAADLW-uwe-vKvEiduk62H2ZU4gg"


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

    def upload_files_to_disk(self, directory):
        self.create_directory('Photo_vk')
        files = os.listdir(directory)
        upload_photo_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for file_name in files:
            with open(f'{directory}/{file_name}', 'rb') as file:
                href = self._get_upload_link(disk_file_path=directory).get('href', '')
                headers = {
                    "Accept": "application/json",
                    "Authorization": "OAuth " + ya_token
                }
                params = {
                    'path': href,
                    'url': file_name
                }
                response = requests.post(url=upload_photo_url, data=file, headers=headers, params=params)
                # response = requests.post(href, data=file)
                # response.raise_for_status()
                if response.status_code == 201:
                    pprint('Success')
                else:
                    pprint('False')
                return response


if __name__ == '__main__':
    ya = YaUploader(token=ya_token)
    pprint(ya.upload_files_to_disk('images'))




