import os
import math
import time

import requests


class Client:
    def __init__(self, api_url, max_byte_length):
        self.api_url = api_url
        self.max_byte_length = max_byte_length

    def upload_file(self, file_path):
        file_size = os.path.getsize(file_path)
        headers = {"Filename": os.path.basename(file_path)}

        with open(file_path, 'rb') as file:
            start = 0

            # In python2 12/5 equals to 2 if file_size int. So we are casting to float
            chunk_count = math.ceil(float(file_size) / self.max_byte_length)
            print("Total chunk count:", chunk_count)
            retry_timeout = 1
            sent_chunk_count = 0

            while True:
                end = min(file_size, start + self.max_byte_length)
                headers['Range'] = "bytes={}-{}/{}".format(start, end, file_size)

                file.seek(start)
                data = file.read(self.max_byte_length)
                start = end

                upload_endpoint = os.path.join(self.api_url, 'content', 'upload')

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
                    return True

            return False
