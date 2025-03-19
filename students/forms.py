"""
Author: Keerthana Thangavelu (C0932267)
Description: This file contains the forms for the 'students' app.
"""
from django import forms
from .models import Student, Marks


class StudentForm(forms.ModelForm):
    """
    A Django form for creating and updating Student instances.

    This form allows users to input and validate data for the Student model.

    Meta:
        model (Student): The model associated with this form.
        fields (list of str): The fields of the model to be included in the form.
    """
    class Meta:
        model = Student
        fields = ['name', 'student_class']

    student_class = forms.ChoiceField(choices=Student.CLASS_CHOICES)  # Use choices from the model


class MarksForm(forms.ModelForm):
    """
    A Django form for creating and updating Marks instances.

    This form allows users to input and validate data for the Marks model.

    Meta:
        model (Marks): The model associated with this form.
        fields (list of str): The fields of the model to be included in the form.
    """
    class Meta:
        model = Marks
        fields = ['english', 'maths', 'physics', 'chemistry', 'computer']
