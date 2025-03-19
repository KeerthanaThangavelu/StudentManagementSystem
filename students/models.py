"""
Author: Keerthana Thangavelu (C0932267)
Description: This file contains the models for the 'students' app.
"""
from django.db import models


class Student(models.Model):
    """
        Model representing a student.

        Attributes:
            name (str): The name of the student.
            student_class (str): The class the student is in.
            score (float): The average score of the student across subjects.
            grade (str): The grade of the student based on their score.
    """

    CLASS_CHOICES = [(i, str(i)) for i in range(1, 13)]  # Choices from 1 to 12

    name = models.CharField(max_length=100)
    student_class = models.IntegerField(choices=CLASS_CHOICES)  # Update field type and choices
    score = models.FloatField(default=0.0)
    grade = models.CharField(max_length=2)

    def __str__(self):
        """
            Returns the string representation of the student object.

            Returns:
                str: The name of the student.
        """
        return self.name

    def update_score_and_grade(self):
        """
            Updates the student's score and grade based on their marks.

            This method checks if the student has associated marks. If so, it calculates
            the score and grade using the marks' methods and saves the student object.
        """
        if hasattr(self, 'marks'):
            self.score = self.marks.calculate_score()
            self.grade = self.marks.calculate_grade()
            self.save()


class Marks(models.Model):
    """
        Model representing the marks of a student in various subjects.

        Attributes:
            student (Student): The student associated with these marks.
            english (int): Marks scored in English.
            maths (int): Marks scored in Mathematics.
            physics (int): Marks scored in Physics.
            chemistry (int): Marks scored in Chemistry.
            computer (int): Marks scored in Computer Science.
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    english = models.IntegerField(default=0)
    maths = models.IntegerField(default=0)
    physics = models.IntegerField(default=0)
    chemistry = models.IntegerField(default=0)
    computer = models.IntegerField(default=0)

    def _str_(self):
        """
            Returns the string representation of the marks object.

            Returns:
                str: The name of the student followed by "'s Marks".
        """
        return f"{self.student.name}'s Marks"

    def calculate_score(self):
        """

        Calculates the average score from all subjects.

        Returns:
            float: The average score across all subjects.
        """
        return (self.english + self.maths + self.physics + self.chemistry + self.computer) / 5

    def calculate_grade(self):
        """
        Calculates the grade based on the average score.

        Returns:
            str: The grade based on the score range.
        """
        score = self.calculate_score()
        if 90 <= score <= 100:
            return 'A'
        elif 80 <= score < 90:
            return 'B'
        elif 70 <= score < 80:
            return 'C'
        elif 50 <= score < 70:
            return 'E'
        else:
            return 'F'
