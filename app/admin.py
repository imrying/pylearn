from django.contrib import admin


from .models import *

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(SchoolClass)
admin.site.register(Assignment)
admin.site.register(Test)
admin.site.register(TestCase)



# Register your models here.
