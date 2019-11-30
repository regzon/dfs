from django.http import HttpResponse
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
