#coding: utf-8

import requests
import re
from io import BytesIO
from storagex.backend.base_backend import BaseBackend


class BaiduShiTuBackEnd(BaseBackend):

    def upload_piece(self, content):
        url = 'http://image.baidu.com/pictureup/uploadshitu'
        files = {}
        files['image'] = ("test.png", content)
        c = requests.post(url, files=files)
        geturl1 = re.sub('%3A', ':', re.findall('queryImageUrl=(.*?)&querySign', c.url)[0])
        realurl = re.sub('%2F', '/', geturl1)
        c.close()
        return realurl


    def download_peice(self, piece_key):

        r = requests.get(piece_key)
        content = r.content
        r.close()
        return content


if __name__ == '__main__':
    with open("/tmp/test.png", 'rb') as f:
        data = f.read()
        print("uploading")
        backend = BaiduShiTuBackEnd()
        piece_key = backend.upload_piece(data)
        print(piece_key)
        down_data = backend.download_peice(piece_key)
        print(len(down_data))

