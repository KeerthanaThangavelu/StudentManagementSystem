"""
Author: Keerthana Thangavelu (C0932267)
"""
from django.contrib import admin

from students.models import Student, Marks

# Register the Student model with the Django admin site
admin.site.register(Student)
# Register the Marks model with the Django admin site
admin.site.register(Marks)
