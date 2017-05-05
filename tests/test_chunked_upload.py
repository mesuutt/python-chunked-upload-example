import os
import unittest

import config

from client import Client

TEST_DIR = os.path.join(config.APP_DIR, 'tests')


class TestFileUpload(unittest.TestCase):

    def setUp(self):
        self.client = Client(config.API_URL, config.MAX_UPLOAD_BYTE_LENGHT)

    def test_single_chunk_file_upload(self):
        print('Testing single chunk file upload')

        file_path = os.path.join(TEST_DIR, 'data', '1MB.file')
        self.client.upload_file(file_path)
        file_size = os.path.getsize(file_path)

        file_name = os.path.basename(file_path)
        uploaded_file_size = os.path.getsize(os.path.join(config.MEDIA_ROOT, file_name))

        self.assertEqual(file_size, uploaded_file_size)

    def test_multiple_chunk_file_upload(self):
        print('Testing multiple chunk upload')

        file_path = os.path.join(TEST_DIR, 'data', '5MB.file')
        self.client.upload_file(file_path)
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        uploaded_file_size = os.path.getsize(os.path.join(config.MEDIA_ROOT, file_name))

        self.assertEqual(file_size, uploaded_file_size)
