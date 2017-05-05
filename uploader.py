import os
import math
import sys
import time

import requests

import config


def upload_file(file_path):
    file_size = os.path.getsize(file_path)
    headers = {"Filename": os.path.basename(file_path)}

    with open(file_path, 'rb') as file:
        start = 0
        chunk_count = math.ceil(file_size / config.MAX_UPLOAD_BYTE_LENGHT)
        print("Total chunk count:", chunk_count)

        retry_timeout = 1
        sent_chunk_count = 0
        while True:
            end = min(file_size, start + config.MAX_UPLOAD_BYTE_LENGHT)
            headers['Range'] = "bytes={}-{}/{}".format(start, end, file_size)

            file.seek(start)
            data = file.read(end)
            start = end

            upload_endpoint = os.path.join(config.API_URL, 'content', 'upload')

            try:
                response = requests.post(upload_endpoint, headers=headers, data=data)
                if response.ok:
                    print('{}. chunk sent to server'.format(sent_chunk_count + 1))
                    sent_chunk_count += 1
            except requests.exceptions.RequestException:
                print('Error while sending chunk to server. Retrying in {} seconds'.format(retry_timeout))
                time.sleep(retry_timeout)

                # Sleep for max 10 seconds
                if retry_timeout < 10:
                    retry_timeout += 1
                continue

            if sent_chunk_count >= chunk_count:
                break


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        TEST_DIR = os.path.join(config.APP_DIR, 'tests')
        file_path = os.path.join(TEST_DIR, 'data', '5MB.file')

    print('Uploading file:', file_path)
    upload_file(file_path)
