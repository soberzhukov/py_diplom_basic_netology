from vk_api import VkApi
from yandex_api import YaDisk
from progress.bar import IncrementalBar


if __name__ == '__main__':
    bar = IncrementalBar('Countdown', max=3)
    VERS = 5.131
    vk_1 = VkApi(TOKEN_VK, VERS)
    photo_list = vk_1.photos_get(112)
    bar.next()
    uploader = YaDisk(TOKEN_YD)
    bar.next()
    uploader.upload(photo_list, 'pho')
    bar.next()
    bar.finish()
