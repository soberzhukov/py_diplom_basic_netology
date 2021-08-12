import requests
from progress.bar import IncrementalBar


class VkApi:
    URL = r'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_id(self):
        METHOD = 'users.get'
        my_id = requests.get(self.URL + METHOD, params={**self.params})
        my_id.raise_for_status()
        VkApi.vk_error(my_id.json())
        return my_id.json()['response'][0]['id']

    def photos_get(self, user_id=None, count_photo=3, album_id='profile'):
        METHOD = 'photos.get'
        params = {
            'owner_id': user_id,
            'album_id': album_id,
            'extended': 1,
        }
        res = requests.get(self.URL + METHOD, params={**self.params, **params})
        res.raise_for_status()
        VkApi.vk_error(res.json())
        result_list = list()
        bar = IncrementalBar('VK_Process', max=len(res.json()['response']['items']))
        for photo_info in res.json()['response']['items']:
            photo_dict = VkApi.max_sizes(photo_info['sizes'])
            name = str(photo_info['likes']['count'])
            dubler = [i for i in result_list if i.get('name') == str(photo_info['likes']['count'])]
            if dubler:
                new_dubler = dubler[0]
                new_dubler['name'] = f"{photo_info['likes']['count']}_{new_dubler['date']}"
                result_list.append(new_dubler)
                result_list.remove(*dubler)
                name = f"{photo_info['likes']['count']}_{photo_info['date']}"
            name_photo_dict = {
                'name': name + '.jpeg',
                'url': photo_dict['url'],
                'size': photo_dict['type'],
                'date': photo_info['date']
            }
            result_list.append(name_photo_dict)
            bar.next()
        bar.finish()
        return result_list[:count_photo]

    @staticmethod
    def max_sizes(some):
        type_symbols = 'smxopqryzw'
        return max(some, key=lambda s: type_symbols.index(s['type']))

    @staticmethod
    def vk_error(resp_dict):
        if resp_dict.get('error', False):
            print(f" VK ERROR:  {resp_dict['error']['error_code']}. {resp_dict['error']['error_msg']}")
            raise SystemExit(1)
