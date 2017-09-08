#coding: utf-8


class BaseSerializer(object):

    def __init__(self, width, height):
        self.header_size = 4
        self.width = width
        self.height = height
        self.size = self.width * self.height * 3

    def give_me_a_best_rect(self, content_size):
        """
        if content_size is larger, extends space
        :param content_size:
        :return:
        """
        original_height = self.height
        while content_size > self.get_data_space_size():
            self.height = self.height + original_height


    def get_header_size(self):
        return self.header_size

    def get_data_space_size(self):
        return self.size - self.header_size

    def serialize(self, data):
        pass

    def unserialize(self, data):
        pass