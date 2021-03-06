from django.db import models
from django.core.validators import int_list_validator
from django.db.models.fields import CharField
from django.db.models.fields.files import FileField

# Create your models here.

class Student(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.CharField(max_length=200)

class Teacher(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.CharField(max_length=200)

class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    code = models.CharField(max_length=256)
    results = models.CharField(max_length=1024, blank=True)
    grades = models.CharField(max_length=1024, blank=True)

class TestCase(models.Model):
    input = CharField(max_length=200)
    output = CharField(max_length=200)

class Test(models.Model):
    test_case = models.ForeignKey(TestCase,on_delete=models.CASCADE)

class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200)
    assignment_description = models.CharField(max_length=200)
    input_description = models.CharField(max_length=200)
    output_description = models.CharField(max_length=200)
    limit_description = models.CharField(max_length=200)
    due_date = models.DateField()
    assignment_answers = models.ManyToManyField(Answer, blank=True)
    test = models.ForeignKey(Test,on_delete=models.CASCADE) 

class SchoolClass(models.Model):
    class_name = models.CharField(max_length=200, unique=True)
    class_description = models.CharField(max_length=200)
    class_code = models.CharField(max_length=6, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True)
    assignments = models.ManyToManyField(Assignment, blank = True)

