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
            log_user_in(request, username)

            if usertype == 'teacher':
                teacher = Teacher(email=email, username=username, password_hash=password)
                teacher.save()
                return redirect('/teacher/')
            else:
                student = Student(email=email, username=username, password_hash=password)
                student.save()
                return redirect('/student/')


    return render(request, 'register.html', context)



def login(request):
    context = {
        'error_messages': []
    }

    if request.method == 'POST':
        try:
            usertype = request.POST['usertype']
            username = request.POST['username']
            password = hashlib.sha256(str(request.POST['password']+SIGNING_SALT).encode('utf8')).hexdigest()
            
            if usertype == 'teacher':
                if Teacher.objects.get(username=username).password_hash == password:
                    log_user_in(request, username)
                    return redirect('/teacher/')

            else:
                if Student.objects.get(username=username).password_hash == password:
                    log_user_in(request, username)
                    return redirect('/student/')
            
        except Exception as e:
            context['error_messages'].append('Fejl i brugernavn eller password')
            print(e)
            username = ""
            password = ""
    
    return render(request, 'login.html', context)

def log_user_in(request, username):
    request.session['username'] = username

def teacher_view(request):
    #teacher = Teacher.objects.get(id=teacher_id)
    username = request.session.get('username')
    if username != None:
        return HttpResponse(username)
    return redirect('/login')

def student_view(request):
    username = request.session.get('username')
    if username != None:
        return HttpResponse(username)
    return redirect('/login')

    