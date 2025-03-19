"""
Author: Keerthana Thangavelu (C0932267)
Description: This file contains the views for the 'students' app.
"""
import csv
import datetime
import io

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from managementsystem import settings
from students.forms import StudentForm, MarksForm
from students.models import Student, Marks
from django.contrib.auth.decorators import login_required

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)


# Create your views here.
@login_required
def student_list(request):
    """
    Display a list of all students.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML of the student list.
    """
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail(request, pk):
    """
    Display the details of a specific student and their marks.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the student to retrieve.

    Returns:
        HttpResponse: Rendered HTML of the student details.
    """
    student = get_object_or_404(Student, pk=pk)
    marks = Marks.objects.get(student=student)
    return render(request, 'students/student_detail.html', {'student': student, 'marks': marks})


@login_required
def student_create(request):
    """
    Create a new student along with their marks.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to the student detail page on success,
                      or renders the student form on failure.
    """
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        marks_form = MarksForm(request.POST)
        if student_form.is_valid() and marks_form.is_valid():
            student = student_form.save()
            marks = marks_form.save(commit=False)
            marks.student = student
            marks.save()
            student.update_score_and_grade()
            return redirect('student_detail', pk=student.pk)
    else:
        student_form = StudentForm()
        marks_form = MarksForm()
    return render(request, 'students/student_form.html', {'student_form': student_form, 'marks_form': marks_form})


@login_required
def student_update(request, pk):
    """
    Update an existing student and their marks.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the student to update.

    Returns:
        HttpResponse: Redirects to the student detail page on success,
                      or renders the student form on failure.
    """
    student = get_object_or_404(Student, pk=pk)
    marks, created = Marks.objects.get_or_create(student=student)

    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        marks_form = MarksForm(request.POST, instance=marks)
        if student_form.is_valid() and marks_form.is_valid():
            student = student_form.save()
            marks = marks_form.save(commit=False)
            marks.student = student
            marks.save()
            student.update_score_and_grade()
            return redirect('student_detail', pk=student.pk)
    else:
        student_form = StudentForm(instance=student)
        marks_form = MarksForm(instance=marks)
    return render(request, 'students/student_form.html', {'student_form': student_form, 'marks_form': marks_form})


@login_required
def student_delete(request, pk):
    """
    Delete a student and their associated marks.

    Args:
        request (HttpRequest): The request object.
        pk (int): The primary key of the student to delete.

    Returns:
        HttpResponse: Redirects to the student list page on success,
                      or renders a confirmation page.
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
def download_report(request):
    """
    Download a CSV report of students filtered by grade.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A CSV file response containing the students' details.
    """
    if request.method == 'POST':
        grade = request.POST['grade']
        students = Student.objects.filter(grade=grade)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="students_grade_{grade}.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['ID', 'Name', 'Class', 'Score', 'Grade', 'English', 'Maths', 'Physics', 'Chemistry', 'Computer'])

        # Create in-memory file
        csv_buffer = io.StringIO()
        writer_s3 = csv.writer(csv_buffer)
        writer_s3.writerow(
            ['ID', 'Name', 'Class', 'Score', 'Grade', 'English', 'Maths', 'Physics', 'Chemistry', 'Computer'])

        for student in students:
            marks = student.marks
            writer_s3.writerow([student.id, student.name, student.student_class, student.score, student.grade,
                                marks.english, marks.maths, marks.physics, marks.chemistry, marks.computer])

        # Move to the beginning of the file
        csv_buffer.seek(0)

        # Generate unique filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        file_name = f'student_reports/students_grade_{grade}_{timestamp}.csv'

        # Upload file to S3
        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=file_name,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )

        for student in students:
            marks = student.marks
            writer.writerow([student.id, student.name, student.student_class, student.score, student.grade,
                             marks.english, marks.maths, marks.physics, marks.chemistry, marks.computer])

        return response

    # Fetch list of files from S3
    files = []
    response = s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="student_reports/")
    if 'Contents' in response:
        for obj in response['Contents']:
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{obj['Key']}"
            files.append({
                'name': obj['Key'].split('/')[-1],
                'url': file_url,
                'last_modified': obj['LastModified'],
                'key': obj['Key'],  # Full S3 key for downloading
            })

    return render(request, 'students/download_report.html', {'files': files})


def download_s3_file(request, file_key):
    """
    Download a file from AWS S3 and serve it as an HTTP response.

    Args:
        request (HttpRequest): The request object.
        file_key (str): The S3 key (file path) of the file.

    Returns:
        HttpResponse: The file as an attachment.
    """

    try:
        file_obj = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        response = HttpResponse(file_obj['Body'].read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_key.split("/")[-1]}"'
        return response
    except (NoCredentialsError, ClientError) as e:
        return HttpResponse(f"Error downloading file: {str(e)}", status=500)

