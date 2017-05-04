import os
import unittest

import config

from uploader import upload_file

TEST_DIR = os.path.join(config.APP_DIR, 'tests')


class TestFileUpload(unittest.TestCase):

    def test_single_chunk_file_upload(self):
        print('Testing single chunk file upload')

        file_path = os.path.join(TEST_DIR, 'data', '1M.file')
        upload_file(file_path)
        file_size = os.path.getsize(file_path)

        file_name = os.path.basename(file_path)
        uploaded_file_size = os.path.getsize(os.path.join(config.MEDIA_ROOT, file_name))

        self.assertEqual(file_size, uploaded_file_size)

    def test_multiple_chunk_file_upload(self):
        print('Testing multiple chunk upload')

        file_path = os.path.join(TEST_DIR, 'data', '5M.file')
        upload_file(file_path)
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        uploaded_file_size = os.path.getsize(os.path.join(config.MEDIA_ROOT, file_name))

        self.assertEqual(file_size, uploaded_file_size)
