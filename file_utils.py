# coding: utf-8

import base64

def get_base64_from_file(filepath):
    with open(filepath, "rb") as f:
        bytes_content = f.read() # bytes
        bytes_64 = base64.b64encode(bytes_content)
    return bytes_64.decode('utf-8') # bytes--->str  (remove `b`)

def get_base85_from_file(filepath):
    with open(filepath, "rb") as f:
        bytes_content = f.read() # bytes
        bytes_85 = base64.b85encode(bytes_content)
    return bytes_85.decode('utf-8') # bytes--->str  (remove `b`)

def covert_base64_to_file(str_base64, to_file):
    bytes_64 = str_base64.encode('utf-8') # str---> bytes (add `b`)
    bytes_content = base64.decodebytes(bytes_64) # bytes
    with open(to_file, "wb") as f:
        f.write(bytes_content)

def covert_base85_to_file(str_base85, to_file):
    bytes_85 = str_base85.encode('utf-8') # str---> bytes (add `b`)
    bytes_content = base64.b85decode(bytes_85) # bytes
    with open(to_file, "wb") as f:
        f.write(bytes_content)


# a = get_base64_str_from_file('C:\\Users\\fakeQ\\Desktop\\11.png')
# save_base64_str_to_file(a,'C:\\Users\\fakeQ\\Desktop\\33.png')
#
# a = get_base85_str_from_file('C:\\Users\\fakeQ\\Desktop\\11.png')
# save_base85_str_to_file(a,'C:\\Users\\fakeQ\\Desktop\\33.png')