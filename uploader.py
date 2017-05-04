import os
import math
import sys

import requests

import config


def upload_file(file_path):
    file_size = os.path.getsize(file_path)
    headers = {"Filename": os.path.basename(file_path)}

    with open(file_path, 'rb') as file:
        start = 0
        chunk_count = math.ceil(file_size / config.MAX_UPLOAD_BYTE_LENGHT)
        print("Total chunk count:", chunk_count)

        for i in range(chunk_count):
            end = min(file_size, start + config.MAX_UPLOAD_BYTE_LENGHT)
            headers['Range'] = "bytes={}-{}/{}".format(start, end, file_size)
            # print(headers)

            file.seek(start)
            data = file.read(end)

            upload_endpoint = os.path.join(config.API_URL, 'content', 'upload')

            response = requests.post(upload_endpoint, headers=headers, data=data)
            if response.ok:
                print('{}. chunk sent to server'.format(i + 1))

            start = end


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        TEST_DIR = os.path.join(config.APP_DIR, 'tests')
        file_path = os.path.join(TEST_DIR, 'data', '5M.file')

    print('Uploading file:', file_path)
    upload_file(file_path)
