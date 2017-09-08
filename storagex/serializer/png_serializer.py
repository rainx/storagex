#coding: utf-8

from storagex.serializer.base_serializer import BaseSerializer
import six
from PIL import Image, ImageMode
from io import BytesIO
import struct


class OverMaxSizeException(Exception):
    pass

"""

|header: 4bytes | data: self.size - 4 |

"""

class PngSerializer(BaseSerializer):

    def serialize(self, data):
        if type(data) is six.text_type:
            data = data.encode("utf-8")

        data_size = len(data)

        if data_size > self.get_data_space_size():
            raise OverMaxSizeException("over size")

        data = struct.pack("<I{}s".format(self.get_data_space_size()), data_size, data)
        img = Image.frombytes("RGB", (self.width, self.height), data, decoder_name='raw')
        outfp = BytesIO()
        img.save(outfp, "png")
        outfp.seek(0)
        return outfp.read()


    def unserialize(self, data):
        infp= BytesIO()
        infp.write(data)
        infp.seek(0)
        img = Image.open(infp)
        raw_data = img.tobytes(encoder_name='raw')
        (size, )  = struct.unpack("<I", raw_data[:4])
        data = raw_data[4:4 + size]
        return data

if __name__ == '__main__':
    source = """
Image Module
The Image module provides a class with the same name which is used to represent a PIL image. The module also provides a number of factory functions, including functions to load images from files, and to create new images.

Examples
The following script loads an image, rotates it 45 degrees, and displays it using an external viewer (usually xv on Unix, and the paint program on Windows).

Open, rotate, and display an image (using the default viewer)
from PIL import Image
im = Image.open("bride.jpg")
im.rotate(45).show()
The following script creates nice 128x128 thumbnails of all JPEG images in the current directory.
    """

    serial = PngSerializer(width=100, height=100)
    data = serial.serialize(source)
    print(data)

    with open("/tmp/out.png", 'wb') as f:
        f.write(data)

    out_data = serial.unserialize(data)

    print(out_data)
