# coding:utf-8

from storagex.backend.baidushitu_backend import BaiduShiTuBackEnd
from storagex.file_meta_info import FileMetaInfo
from storagex.serializer.png_serializer import PngSerializer
import os
import click
import datetime

class Storage(object):

    def __init__(self, width=1024, height=768, backtend='baidu_shitu'):
        if backtend == 'baidu_shitu':
            self.backend = BaiduShiTuBackEnd()
        else:
            raise NotImplementedError("not available backend")

        self.width = width
        self.height = height
        self.serializer = PngSerializer(width, height)
        self.verbose = False

    def put_file(self, file_name):
        if not os.path.isfile(file_name):
            self.echo("not a file : ".format(file_name))
            return False
        file_info = os.stat(file_name)
        file_total_size = file_info.st_size
        self.echo("total file size is {}".format(file_total_size))
        meta = FileMetaInfo()
        meta.piece_width = self.width
        meta.piece_height = self.height
        meta.filename = os.path.basename(file_name)
        data_space_size = self.serializer.get_data_space_size()
        with open(file_name, 'rb') as f:
            seq = 0
            offset = 0
            while True:
                piece_data = f.read(data_space_size)
                piece_data_size = len(piece_data)

                self.echo("seq {} size is {}".format(seq, piece_data_size))
                if piece_data == b"":
                    break
                piece_key = self.backend.upload_piece(self.serializer.serialize(piece_data))
                meta.add_piece(seq, key=piece_key, offset=offset, size=piece_data_size, checksum="")
                offset += piece_data_size
                self.echo("upload seq {} done, percent is {}%".format(seq, (offset/file_total_size) * 100))
                seq += 1

        meta_info_key = self.backend.upload_piece(self.serializer.serialize(meta.to_json()))
        self.echo("meta is : {}".format(meta.to_json()))
        self.echo("meta key is : {} ".format(meta_info_key))
        return meta_info_key, meta


    def get_meta(self, meta_info_key):
        meta_info_data = self.backend.download_peice(piece_key=meta_info_key)
        meta_info = FileMetaInfo()
        meta_info.from_json(self.serializer.unserialize(meta_info_data).decode("utf-8"))
        return meta_info

    def get_content(self, meta_info_key):
        meta_info = self.get_meta(meta_info_key)
        content = bytearray()
        for piece in meta_info.pieces:
            self.echo("downloading piece {} .. ".format(piece['seq']))
            one_piece_data = self.serializer.unserialize(self.backend.download_peice(piece['key']))
            content.extend(one_piece_data)
        return content

    def download_file(self, meta_info_key, file_name):
        with open(file_name, "wb") as f:
            f.write(self.get_content(meta_info_key))
            return f
        return False

    def echo(self, *args):
        if self.verbose:
            one = "{} [storagex] ".format(datetime.datetime.now()) + args[0]
            other_args = args[1:]
            click.echo(one, *other_args)

if __name__ == '__main__':
    storage = Storage(width=300, height=300)
    storage.verbose = True
    # meta_info_key = storage.put_file("/Users/rainx/Downloads/期货市场基础知识.pptx")
    # print(meta_info_key)

    meta = storage.get_meta("http://e.hiphotos.baidu.com/image/pic/item/77c6a7efce1b9d16894ca05ef8deb48f8c546401.jpg")
    print(meta.to_json())

    storage.download_file("http://e.hiphotos.baidu.com/image/pic/item/77c6a7efce1b9d16894ca05ef8deb48f8c546401.jpg", "/tmp/test.pptx")