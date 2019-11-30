from django.http import JsonResponse
import json

DEF_SIZE = 1024


def init(request):
    if request.method == 'POST':
        data = {
            'status': 'success',
            'data': {
                'size': DEF_SIZE
            }
        }
    else:
        data = {
            'status': 'error',
            'message': f'Not correct method type.\
                 Get {request.method} insted POST'
        }
    return JsonResponse(data)


def create_file(request):
    if request.method == 'POST':
        # TODO: get from Storage server
        upload_url = ''
        data = {
            'status': 'success',
            'data': {
                'upload_url': upload_url
            }
        }
    else:
        data = {
            'status': 'error',
            'message': f'Not correct method type.\
            Get {request.method} insted POST'
        }
    return JsonResponse(data)


def read_file(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']
        if file_exists(path):
            # TODO: get from Storage server
            url_to_file = ''
            data = {
                'status': 'success',
                'data': {
                    'download_url': url_to_file
                }
            }
        else:
            data = {'status': 'error', 'message': 'Path/File does not exist'}

    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted GET'
                }

    return JsonResponse(data)


def write_file(request):
    if request.method == 'POST':
        # TODO: get from Stroage server
        url_to_upload_file = ''
        data = {
            'status': 'success',
            'data': {
                'upload_url': url_to_upload_file
            }
        }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted POST'
                }

    return JsonResponse(data)


def delete_file(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']

        if file_exists(path):
            # TODO: send request to Storage server to delete
            data = {'status': 'success'}
        else:
            data = {'status': 'error',
                    'message': 'Path/File does not exist'
                    }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted POST'
                }

    return JsonResponse(data)


def get_file_info(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']

        if file_exists(path):
            size = get_file_size(path)
            # TODO: send request to Storage server to delete
            data = {
                'status': 'success',
                'data': {
                    'size': size,
                }
            }
        else:
            data = {
                'status': 'error',
                'message': 'File does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted GET'
                }
    return JsonResponse(data)


def copy_file(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        source = body['source_path']
        dest = body['destination_path']

        if dir_exists(source) and dir_exists(dest):
            data = {'status': 'success'}
        else:
            data = {
                'status': 'error',
                'message': 'Directory does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted POST'
                }
    return JsonResponse(data)


def read_dir(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']
        filenames = get_filenames(path)
        if dir_exists(path):
            data = {
                'status': 'success',
                'data': {
                    'filenames': filenames
                }
            }
        else:
            data = {
                'status': 'error',
                'message': 'Directory does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted GET'
                }

    return JsonResponse(data)


def create_dir(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']
        # TODO: check path correctness
        if not dir_exists(path):
            data = {'status': 'success'}
        else:
            data = {
                'status': 'error',
                'message': f'Invalid directory path: Directory {path}'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                insted POST'
                }

    return JsonResponse(data)


# TODO Ask for confirm deletion
def delete_dir(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']

        if dir_exists(path):
            data = {'status': 'success'}
        else:
            data = {
                'status': 'error',
                'message': 'Directory does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                insted POST'
                }
    return JsonResponse(data)


def file_exists(file_path):
    return True


def get_filenames(dir_path):
    return None


def dir_exists(path):
    return True


def get_file_size(path):
    return -1
