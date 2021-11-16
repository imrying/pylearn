from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import hashlib

from .models import *

from pylearn.settings import SIGNING_SALT

def register(request):
    context = {
        'error_messages': []
    }

    if request.method == 'POST':
        try:
            usertype = request.POST['usertype']
            print(usertype)
            email = request.POST['email']
            username = request.POST['username']
            password = hashlib.sha256(str(request.POST['password']+SIGNING_SALT).encode('utf8')).hexdigest()
            cpassword = hashlib.sha256(str(request.POST['cpassword']+SIGNING_SALT).encode('utf8')).hexdigest()
            context['username']=username
            context['password']=password
        except Exception as e:
            print(e)
            email = ""
            username = ""
            password = ""
            cpassword = ""
            context['error_messages'].append('Venligst udfyld alle felter korrekt')

        # check if username exists

        # check if email is valid

        # check if password is valid

        # check if password equals confirm-password
        if password != cpassword:
            context['error_messages'].append('Passwords matcher ikke')

        #everything worked. Add the teacher to db.
        
        if len(context['error_messages']) == 0:
            log_user_in(request, email, username)

            if usertype == 'teacher':
                teacher = Teacher(email=email, username=username, password_hash=password)
                teacher.save()
                return redirect(f'/teacher/')
            else:
                student = Student(email=email, username=username, password_hash=password)
                student.save()
                return redirect(f'/student')


    return render(request, 'register.html', context)



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
        # if Teacher.objects.get(username) == username
    
        #context = {'username': username, 'password': password}
    
    return render(request, 'login.html')

def log_user_in(request, email, username):
    request.session['email'] = email
    request.session['username'] = username

def teacher_view(request):
    #teacher = Teacher.objects.get(id=teacher_id)
    email = request.session.get('email')
    if email != None:
        return HttpResponse(email)
    return redirect('/login')
    