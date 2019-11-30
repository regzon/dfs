from django.http import HttpResponse
import json

DEF_SIZE = 1024


def init(request):
    response = HttpResponse()
    if request.method == 'POST':
        response['status'] = 'successs'
        response['data']['size'] = DEF_SIZE
    else:
        response['status'] = 'error'
        response['error'] = f'Not correct method type. Get {request.method}\
            insted POST'


def create_file(request):
    response = HttpResponse()
    if request.method == 'POST':
        # TODO: get from StorageNode
        upload_url = ''
        response['status'] = 'success'
        response['data']['upload_url'] = upload_url
    else:
        response['status'] = 'error'
        response['error'] = f'Not correct method type. Get {request.method}\
            insted POST'


def read_file(request):
    response = HttpResponse()
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']
        if is_exists(path):
            # TODO: get from StorageNode
            url_to_file = ''
            response['status'] = 'success'
            response['data']['download_url'] = url_to_file
        else:
            response['status'] = 'error'
            response['error'] = 'Path/File does not exists'

    else:
        response['status'] = 'error'
        response['error'] = f'Not correct method type. Get {request.method}\
            insted GET'


def is_exists(file_path):
    pass
