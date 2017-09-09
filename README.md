# StorageX

## Installable

```bash
pip install storagex 
```

## CommandLine

### Upload file

```bash
-->rainx@JingdeMacBook-Pro:~/dev/storagex$ storagex upload /tmp/sz000001 
2017-09-08 23:21:45.570764 [storagex] total file size is 0
2017-09-08 23:21:45.571984 [storagex] seq 0 size is 0
2017-09-08 23:21:47.833424 [storagex] meta is : {"piece_width": 1024, "protocol_version": 1.0, "pieces": [], "piece_height": 768, "filename": "sz000001"}
2017-09-08 23:21:47.833511 [storagex] meta key is : http://f.hiphotos.baidu.com/image/pic/item/1b4c510fd9f9d72a455d3a22df2a2834349bbbd7.jpg 
Completely uploaded! YOUR DOWNLOAD KEY IS : http://f.hiphotos.baidu.com/image/pic/item/1b4c510fd9f9d72a455d3a22df2a2834349bbbd7.jpg
```

### Download File

```bash
-->rainx@JingdeMacBook-Pro:~/dev/storagex [master]$ storagex download http://f.hiphotos.baidu.com/image/pic/item/1b4c510fd9f9d72a455d3a22df2a2834349bbbd7.jpg /tmp/sz000001.backup
{"piece_width": 1024, "protocol_version": 1.0, "pieces": [], "piece_height": 768, "filename": "sz000001"}
donwload done! the file is /tmp/sz000001.backup
```

## API

### Upload file

```python
from storagex.storage import Storage

storage = Storage(width=600, height=600) 
# width and height will decide the chunk size ,one chunk size will be `width * height * 3 - 4`
key, meta_info = storage.upload(file_name)
```
### Download file

```python
from storagex.storage import Storage

storage = Storage()
storage.download_file(meta_info_key, file_name)
```

## WorkFlow

### Upload Workflow

```
+----------------------------------------------------------+
|                          Raw file                        |
+-----------------------------+----------------------------+
                              | split to pieces(size is W x H x 3 - header size)
          +------------------------------------------+
          |                   |                      |
+---------v----+   +----------v----+          +------v-----+
|    piece 1   |   |    piece 2    |          |   piece n  |
+---------+----+   +--------+------+          +------+-----+
          |                 |                        |
          |                 |  serialize(make it uploadable, such as to png format)
          |                 |                        |
+---------v-------------+ +-v---+ +------------------v-----+    +----------------+
|   serialized piece 1  | |  2  | |   serialized piece n   |    | meta info data |
+---------+-------------+ +--+--+ +------------------+-----+    +--^---+---------+
          |                  |                       |             |   |
          | upload and gen key(keys will be save to meta info+-----+   |serialize
          |                  +                       +                 |
+---------v------------------v-----------------------v------+    +-----v---------+
|                                                           |    |               |
|                          backend in cyber space           <--+-+ serialized    |
|                                                           |  | | meta info data|
+-----------------------------------------------------------+  | +---------------+
  upload serialized meta info data into backend and gen key   <+
  you need to keep this *key* (meta info data key)
```

### Download Workflow

```
+------------------------------------------------------------+
|                                                            |
|                    backend in cyber space                  |
|                                                            |
+-----------------+---------------------------^--+-----------+
                  | get meta info data by key |  |
+-----------------v--------------+            |  |
|   serialized meta info data    |            |  |
+-----------------+--------------+            |  |
                  | unserialize               |  |
+-----------------v--------------+            |  |
|      meta info data            |            |  |
+--------------------------------+            |  |
  this includes all keys of pieces            |  |
                 +                            |  |
                 |   get all pieces           |  |
                 +----------------------------+  |
                                                 |
                                                 |
 +-------------------------------+---------------+
 |                               |
 |                               |
 |                               |
 v                               v
 +------------------------+     ++-----------------------+
 |  serialized piece 1    | ... |     serialized piece n |
 +------------+-----------+     +-------------+----------+
              |   unserialize                 |
 +------------v-----------+     +-------------v----------+
 |        piece 1         | ... |          piece n       |
 +-----------+------------+     +-------------+----------+
             |          join to raw file      |
             +---------------^----------------+
                             |
 +---------------------------v---------------------------+
 |                      Raw file                         |
 +-------------------------------------------------------+

```