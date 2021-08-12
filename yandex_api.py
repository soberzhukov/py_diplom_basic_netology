import requests
import json
from progress.bar import IncrementalBar


class YaDisk:
    UPLOAD_URL = r'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def upload(self, photos_list, photo_path):
        METHOD = 'upload'
        self.create_dir(photo_path)
        YaDisk.write_to_json(photos_list)
        bar = IncrementalBar('YD_Process', max=len(photos_list))
        for photo in photos_list:
            resp_photo = requests.get(photo['url'])
            resp_photo.raise_for_status()
            photo_content = resp_photo.content
            res = requests.get(self.UPLOAD_URL + METHOD,
                               params={'path': f"/{photo_path}/{photo['name']}",
                                       'overwrite': 'true'},
                               headers={**self.headers}
                               )
            res.raise_for_status()
            href = res.json()['href']
            res1 = requests.put(href, files={'file': photo_content})
            res1.raise_for_status()
            bar.next()
        bar.finish()

    @staticmethod
    def write_to_json(photos_list):
        info_list = list()
        with open('info.json', 'w') as f:
            for photo in photos_list:
                info_list.append({
                    "file_name": photo['name'],
                    "size": photo['size']
                })
            json.dump(info_list, f, indent=2)

    def create_dir(self, path):
        res = requests.get(self.UPLOAD_URL,
                           params={'path': f'/'},
                           headers={**self.headers}
                           )
        res.raise_for_status()
        if path in [i.get('name') for i in res.json()['_embedded']['items']]:
            print(' YD ERROR: Такая директория уже существует')
            raise SystemExit(1)
        res = requests.put(self.UPLOAD_URL,
                           params={'path': f'/{path}'},
                           headers={**self.headers}
                           )
        res.raise_for_status()
        return True
