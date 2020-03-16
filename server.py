import os
import re

from bottle import run, route, request, BaseRequest, response

import config

# Maximum size of memory buffer for request body in bytes.
BaseRequest.MEMFILE_MAX = config.MAX_UPLOAD_BYTE_LENGHT


@route('/content/upload', method='POST')
def upload():
    range_header = request.headers.get('Range')
    match = re.search('(?P<start>\d+)-(?P<end>\d+)/(?P<total_bytes>\d+)', range_header)
    start = int(match.group('start'))
    # end = int(match.group('end'))
    # total_bytes = int(match.group('total_bytes'))

    file_name = os.path.basename(request.headers.get('Filename'))
    file_path = os.path.join(config.MEDIA_ROOT, file_name)
    # append chunk to the file or create file if not exist

    with open(file_path, 'rb+' if os.path.exists(file_path) else 'wb+') as f:
        f.seek(start)
        chunk = request.body.read(config.MAX_UPLOAD_BYTE_LENGHT)
        f.write(chunk)
        # print("start={}, byte_len={}, pos={}".format(start, len(chunk), f.tell()))

    response.status = 200
    return response

run(host=config.HOST, port=config.PORT, debug=True)
