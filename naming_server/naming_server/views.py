from django.http import JsonResponse
import json

DEF_SIZE = 1024


def init(request):
    if request.method == 'POST':
        data = [{'status': 'success', 'data': {'size': DEF_SIZE}}]
    else:
        data = [{'status': 'error', 'error': f'Not correct method type.\
                 Get {request.method} insted POST'}]
    return JsonResponse(data)


def create_file(request):
    if request.method == 'POST':
        # TODO: get from Storage server
        upload_url = ''
        data = [{'status': 'success', 'data': {'upload_url': upload_url}}]
    else:
        data = [{'status': 'error', 'error': f'Not correct method type.\
                 Get {request.method} insted POST'}]
    return JsonResponse(data)


def read_file(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']
        if file_exists(path):
            # TODO: get from Storage server
            url_to_file = ''
            data = [{
                'status': 'success',
                'data': {
                    'download_url': url_to_file
                }
            }]
        else:
            data = [{'status': 'error', 'error': 'Path/File does not exist'}]

    else:
        data = [{'status': 'error',
                 'error': f'Not correct method type. Get {request.method}\
                 insted GET'
                 }]

    return JsonResponse(data)


def file_exists(file_path):
    return True


def write_file(request):
    if request.method == 'POST':
        # TODO: get from Stroage server
        url_to_upload_file = ''
        data = [{
            'status': 'success',
            'data': {
                'download_url': url_to_upload_file
            }
        }]
    else:
        data = [{'status': 'error',
                 'error': f'Not correct method type. Get {request.method}\
                 insted POST'
                 }]

    return JsonResponse(data)


def delete_file(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']

        if file_exists(path):
            # TODO: send request to Storage server to delete
            data = [{'status': 'success'}]
        else:
            data = [{'status': 'error', 'error': 'Path/File does not exist'}]
    else:
        data = [{'status': 'error',
                 'error': f'Not correct method type. Get {request.method}\
                 insted POST'
                 }]

    return JsonResponse(data)
