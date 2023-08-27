from django.http import HttpResponse
import src.app as app
import src.test as test


def start(request):
    app.start()
    # test.start()
    return HttpResponse("ssss")


def stop(request):
    return ''
