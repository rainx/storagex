#coding: utf-8

import json

class FileMetaInfo(object):

    def __init__(self):
        self.protocol_version = 1.0
        self.filename = ""
        self.piece_width = 0
        self.piece_height = 0
        self.pieces = []


    def add_piece(self, seq, key, offset, size, checksum):
        one_piece = {
            'seq': seq,
            'key': key,
            'offset': offset,
            'size': size,
            'checksum': checksum
        }
        self.pieces.append(one_piece)

    def to_json(self):
        obj = {}
        obj['protocol_version'] = self.protocol_version
        obj['filename'] = self.filename
        obj['piece_width'] = self.piece_width
        obj['piece_height'] = self.piece_height
        obj['pieces'] = self.pieces
        return json.dumps(obj)

    def from_json(self, data):
        print(data)
        obj = json.loads(data)
        self.protocol_version = obj['protocol_version']
        self.filename = obj['filename']
        self.piece_width = obj['piece_width']
        self.piece_height = obj['piece_height']
        self.pieces = obj['pieces']


if __name__ == '__main__':
    meta_info = FileMetaInfo()

    meta_info.add_piece(0, 'hello1', 0, 2000, 'wawawa')
    json_data = meta_info.to_json()
    print(json_data)

    new_meta_info = FileMetaInfo()
    info = new_meta_info.from_json(json_data)
    print(json_data)