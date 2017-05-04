import os

HOST = 'localhost'
PORT = 8080

APP_DIR = os.getcwd()
MEDIA_ROOT = os.path.join(APP_DIR, 'media')
MAX_UPLOAD_BYTE_LENGHT = 1024 * 1024  # 1M

API_URL = 'http://{}:{}'.format(HOST, PORT)
