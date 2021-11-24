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

class SchoolClass(models.Model):
    class_name = models.CharField(max_length=200, unique=True)
    class_description = models.CharField(max_length=200)
    class_code = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)


class Test(models.Model):
    test_cases = FileField()
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)

class TestCase(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    input = CharField(max_length=200)
    output = CharField(max_length=200)



