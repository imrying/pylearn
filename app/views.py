from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import hashlib
import random
import string
import json
import re
from django.core.files.storage import FileSystemStorage

from .models import *

from pylearn.settings import SIGNING_SALT

def register(request):
    context = {
        'error_messages': []
    }

    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        db_table = Teacher if usertype == "teacher" else Student

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # hash passwords
        hashed_password = hashlib.sha256(str(
            password+SIGNING_SALT).encode('utf8')).hexdigest()
        hashed_cpassword = hashlib.sha256(str(
            cpassword+SIGNING_SALT).encode('utf8')).hexdigest()

        # add user inputs to context
        context['email'] = email
        context['username'] = username
        context['password'] = password
        context['cpassword'] = cpassword

        # check if username and/or email exists
        uname_exists = db_table.objects.filter(username=username).exists()
        email_exists = db_table.objects.filter(email=email).exists()
        if uname_exists:
            context['error_messages'].append('Brugernavnet eksisterer allerede')
        if email_exists:
            context['error_messages'].append('Emailen eksisterer allerede')

        # check if email is valid
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            context['error_messages'].append('Ugyldig email adresse')

        # check if password is valid
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            context['error_messages'].append('Adgangskoden skal indeholde: Store bogstaver, tal og special karaktere samt være 8 karaktere lang')

        # check if password equals confirm-password
        if hashed_password != hashed_cpassword:
            context['error_messages'].append('Passwords matcher ikke')

        #everything worked. Add the teacher to db.
        if len(context['error_messages']) == 0:
            log_user_in(request, username)

            new_user = db_table(email=email, username=username, password_hash=hashed_password)
            
            new_user.save()

            if usertype == 'teacher':
                return redirect('/teacher/')
            else:
                return redirect('/student/')


    return render(request, 'register.html', context)


def login(request):
    context = {
        'error_messages': []
    }

    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(str(password+SIGNING_SALT).encode('utf8')).hexdigest()
        
        # save username and password to the context
        context['username'] = username
        context['password'] = password

        # check if user exists and then log in
        db_table = Teacher if usertype == "teacher" else Student
        if db_table.objects.filter(username=username, password_hash=hashed_password).exists():
            log_user_in(request, username)
            if usertype == 'teacher':
                return redirect('/teacher/')
            return redirect('/student/')

        context['error_messages'].append('Brugernavn eller password passer ikke')    
    
    return render(request, 'login.html', context)

def log_user_in(request, username):
    request.session['username'] = username

def teacher_view(request):
    username = request.session.get("username")
    context = {'username': username}

    if username == None:
        return redirect('/')
    
    username = request.session.get('username')

    # Find alle lærenes klasser
    teacher_classes = list(filter(lambda x: x.teacher.username == username, SchoolClass.objects.all()))
    context['teacher_classes'] = teacher_classes

    # Find alle lærenes opgaver
    list_of_list_of_assigments = []
    for schoolclass in teacher_classes:
        list_of_list_of_assigments.append(schoolclass.assignments.all())

    _teacher_assignments_ = [assignment for assignmentlist in list_of_list_of_assigments for assignment in assignmentlist]

    teacher_assignments = []
    for i in _teacher_assignments_:
        teacher_assignments.append({
            "name": i.assignment_name,
            "assignment_description": i.assignment_description,
            "input_description": i.input_description,
            "output_description": i.output_description,
            "limit_description": i.limit_description,
            "class_name": i.schoolclass_set.all()[0].class_name,
            "class_code": i.schoolclass_set.all()[0].class_code,
            "due_date": str(i.due_date)
        })

    context['teacher_assignments'] = json.dumps(teacher_assignments)
    return render(request, 'teacher.html', context)

def teacher_create_class(request):
    if request.method == 'POST':
        context = {
            'error_messages': []
        }
        class_name = request.POST.get('class_name')
        if class_name: 
            context['class_name']= class_name

        class_description = request.POST.get('class_description')
        if class_description: 
            context['class_description']= class_description

        teacher = Teacher.objects.get(username=request.session.get('username'))


        if len(class_name) < 1:
            context['error_messages'].append('Indtast venligst et navn')
        if len(class_description) < 50:
            context['error_messages'].append('Beskrivelsen skal min. indeholde 50 tegn')

        if len(context['error_messages']) == 0:
            try:
                new_class = SchoolClass(class_name = class_name, 
                                        class_description = class_description, 
                                        class_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)), 
                                        teacher = teacher)
                new_class.save()
                return redirect('/teacher')
            except Exception as e:
                print(e)
        else:
            return render(request, 'teacher_create_class.html', context)
    
    return render(request, 'teacher_create_class.html')
            
 
def student_view(request):
    username = request.session.get("username")
    context = {'username': username}

    if username == None:
        return redirect('/')
    
    username = request.session.get('username')
    student = Student.objects.get(username=username)

    # Find alle elevens klasser
    #student_classes = list(filter(lambda x: x.students.username == username, SchoolClass.objects.all()))
    student_classes = student.schoolclass_set.all()
    
    context['student_classes'] = student_classes


    assignments = []
    for school_class in student_classes:
        assignments += school_class.assignments.all()

    student_assignments = []
    for i in assignments:
        student_assignments.append({
            "name": i.assignment_name,
            "assignment_description": i.assignment_description,
            "input_description": i.input_description,
            "output_description": i.output_description,
            "limit_description": i.limit_description,
            "class_name": i.schoolclass_set.all()[0].class_name,
            "class_code": i.schoolclass_set.all()[0].class_code,
            "due_date": str(i.due_date)
        })

    context['student_assignments'] = json.dumps(student_assignments)
    return render(request, 'student.html', context)

def student_join_class(request):
    if request.method == 'POST':
        username = request.session.get('username')
        student = next((x for x in Student.objects.all() if x.username == username), None)
        newclass = next((x for x in SchoolClass.objects.all() if x.class_code == request.POST.get('class_code')), None)

        if (newclass == None):
            pass #lav error handling
        else:
            newclass.students.add(student)
            return redirect('/student')
    return render(request, 'student_join_class.html')

def front_page(request):
    
    context = {
        'error_messages': []
    }

    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(str(password+SIGNING_SALT).encode('utf8')).hexdigest()
        
        # save username and password to the context
        context['username'] = username
        context['password'] = password

        # check if user exists and then log in
        db_table = Teacher if usertype == "teacher" else Student
        if db_table.objects.filter(username=username,password_hash=hashed_password).exists():
            log_user_in(request, username)
            if usertype == 'teacher':
                return redirect('/teacher/')
            return redirect('/student/')

        context['error_messages'].append('Brugernavn eller password passer ikke') 

    return render(request, 'front_page.html', context)

def teacher_create_assignment(request):
    username = request.session.get("username")
    context = {'username': username, 'error_messages': []}

    if username == None:
        return redirect('/')
    
    try: 
        teacher_classes = filter(lambda x: x.teacher.username == username, SchoolClass.objects.all())
        context['teacher_classes'] = teacher_classes
    except Exception as e:
        print(e)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            context['name'] = name
        assignment_description = request.POST.get('assignment_description')
        if assignment_description:
            context['assignment_description'] = assignment_description
        input_description = request.POST.get('input_description')
        if input_description:
            context['input_description'] = input_description
        output_description = request.POST.get('output_description')
        if output_description:
            context['output_description'] = output_description
        limit_description = request.POST.get('limit_description')
        if limit_description:
            context['limit_description'] = limit_description
        class_code = request.POST.get('class_name')
        if class_code:
            context['class_code'] = class_code
        due_date = request.POST.get('date')
        if due_date:
            context['due_date'] = due_date
        input_file = request.FILES.get('input_file') 
        output_file = request.FILES.get('output_file')

        # Check for errors
        if len(name) < 1:
            context['error_messages'].append('Venligst angiv et navn til opgaven')
        if len(assignment_description) < 50:
            context['error_messages'].append('Opgave beskrivelsen skal min. indeholde 50 tegn')
        if len(input_description) < 50:
            context['error_messages'].append('Input beskrivelsen skal min. indeholde 50 tegn')
        if len(output_description) < 50:
            context['error_messages'].append('Output beskrivelsen skal min. indeholde 50 tegn')
        if len(limit_description) < 50:
            context['error_messages'].append('Begrænsnings beskrivelsen skal min. indeholde 50 tegn')
        if not class_code:
            context['error_messages'].append('Angiv venligst en klasse')
        if not due_date:
            context['error_messages'].append('Venligst angiv en Afleveringsfrist')
        if not input_file:
            context['error_messages'].append('Venligst upload en input fil')
        if not output_file:
            context['error_messages'].append('Venligst upload en output fil')        

        if len(context['error_messages']) == 0:
            fs = FileSystemStorage()
            input_name = "input" + username + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + input_file.name
            output_name = "output" + username + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + input_file.name
            fs.save(input_name, input_file)
            fs.save(output_name, output_file)
            test_case = TestCase(input=input_name, output=output_name)
            test_case.save()
            test = Test(test_case=test_case)
            test.save()
            print(')============================(')
            print('FAILING AT School class')
            try:
                school_class = SchoolClass.objects.get(class_code=class_code)
            except: 
                # Couldnt find school class
                pass
            print(')============================(')
            print('FAILING AT ASSIGN')
            assignment = Assignment(assignment_name = name, 
                                    assignment_description=assignment_description, 
                                    input_description=input_description,
                                    output_description=output_description,
                                    limit_description=limit_description,
                                    due_date=due_date,
                                    test = test
                                    )
            assignment.save()
            school_class.assignments.add(assignment)
            school_class.save()
            return redirect('/teacher/')
        else:
            return render(request, 'teacher_create_assignment.html', context)

    return render(request, 'teacher_create_assignment.html', context)
    