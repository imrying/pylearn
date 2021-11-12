from django.shortcuts import redirect, render
import hashlib

from pylearn.settings import SIGNING_SALT


def login(request):

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = hashlib.sha256(str(request.POST['password']+SIGNING_SALT).encode('utf8')).hexdigest()
            print(username)
            print(password)
        except Exception as e:
            print(e)
            username = ""
            password = ""
        # check if user is valid if it is redirect
        if username != '':
            return redirect('https://google.com')
    
        #context = {'username': username, 'password': password}
    
    return render(request, 'login.html')


    

    