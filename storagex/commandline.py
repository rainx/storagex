#coding: utf-8

import click
from storagex.storage import Storage


@click.group()
def storagex():
    pass

@storagex.command()
#@click.option('-f', '--filename', help="file to upload")
@click.argument('filename')
def upload(filename):
    storage = Storage(1024, 768)
    storage.verbose = True
    ret = storage.put_file(filename)
    if ret is not False and ret[0] is not None:
        click.secho("Completely uploaded! YOUR DOWNLOAD KEY IS : {}".format(ret[0]), fg="green")


@storagex.command()
# @click.option('-k', '--key', help="Download Key")
# @click.option('-f', '--filename', help="file name of download file")
@click.argument("key")
@click.argument("filename")
def download(key, filename):
    storage = Storage(1024, 768)
    storage.verbose = True
    if storage.download_file(meta_info_key=key, file_name=filename) is not False:
        click.secho("donwload done! the file is {}".format(filename), fg='green')