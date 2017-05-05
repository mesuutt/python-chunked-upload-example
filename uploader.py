import os
import sys

import config
from client import Client

if __name__ == '__main__':
    client = Client(config.API_URL, config.MAX_UPLOAD_BYTE_LENGHT)

    try:
        file_path = sys.argv[1]
    except IndexError:
        TEST_DIR = os.path.join(config.APP_DIR, 'tests')
        file_path = os.path.join(TEST_DIR, 'data', '5MB.file')

    print('Uploading file:', file_path)
    client.upload_file(file_path)
