# students/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student, Marks

#smspostgres
#B1FXk6wYovmepzyxabDQ

class StudentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.student = Student.objects.create(name='John Doe', student_class='10', score=85, grade='B')
        self.marks = Marks.objects.create(
            student=self.student,
            english=80,
            maths=90,
            physics=85,
            chemistry=75,
            computer=88
        )

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, self.student.name)

    def test_student_detail_view(self):
        response = self.client.get(reverse('student_detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, self.student.name)
        self.assertContains(response, self.marks.english)

    def test_student_create_view(self):
        data = {
            'name': 'Jane Smith',
            'student_class': '9',
            'english': 85,
            'maths': 90,
            'physics': 78,
            'chemistry': 85,
            'computer': 92,
        }
        response = self.client.post(reverse('student_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Student.objects.filter(name='Jane Smith').exists())
        self.assertTrue(Marks.objects.filter(student__name='Jane Smith').exists())

    def test_student_update_view(self):
        data = {
            'name': 'John Doe Updated',
            'student_class': '11',
            'english': 85,
            'maths': 88,
            'physics': 90,
            'chemistry': 80,
            'computer': 87,
        }
        response = self.client.post(reverse('student_update', kwargs={'pk': self.student.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'John Doe Updated')

    def test_student_delete_view(self):
        response = self.client.post(reverse('student_delete', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_download_report_view(self):
        response = self.client.post(reverse('download_report'), {'grade': 'B'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename="students_grade_B.csv"'))
        self.assertIn(b'ID,Name,Class,Score,Grade,English,Maths,Physics,Chemistry,Computer', response.content)
        self.assertIn(bytes(str(self.student.id), 'utf-8'), response.content)

    def test_download_report_view_no_grade(self):
        response = self.client.get(reverse('download_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/download_report.html')