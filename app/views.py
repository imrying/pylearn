from django.shortcuts import render
import hashlib

from pylearn.settings import SIGNING_SALT


def login(request):

    try:
        username = request.POST['username']
        password = hashlib.sha256(str(request.POST['password']+SIGNING_SALT).encode('utf8')).hexdigest()
        print(username)
        print(password)
    except Exception as e:
        print(e)
        username = ""
        password = ""

    context = {'username': username, 'password': password}

    return render(request, 'login.html', context)