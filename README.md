## Student Management System

This project is a web-based application developed using Django for managing student information. The application provides features to create, read, update, and delete (CRUD) student records. Additionally, it includes a report generation feature where users can download student reports based on specific conditions such as score and grade.

### Technical Requirements

#### Technologies Used

-	Frontend: HTML5, CSS3, Bootstrap, JavaScript
-	Backend: Python (Django Framework)
-	Database: AWS RDS with Postgres
-	Cloud Hosting: AWS EC2 (Ubuntu Server)
-	Storage: AWS S3 for media and file uploads


### System Architecture and Design

- *Models*: Defines the structure of the student data.
- *Views*: Handles the business logic and interactions.
- *Templates*: Renders HTML pages to be displayed to the user.
- *URLs*: Maps URL paths to the corresponding views.

## Project Structure

    .
    ├── templates                           
    │   ├── registration                    
    │   │   └── login.html                  # Template for user login.
    │   ├── students                        
    │   │   ├── download_report.html        # Template for downloading student reports.
    │   │   ├── student_confirm_delete.html # Template for confirming student deletion.
    │   │   ├── student_detail.html         # Template to show details of a student.
    │   │   ├── student_form.html           # Template for adding or updating a student.
    │   │   └── student_list.html           # Template to list all students.
    │   └── base.html                       # Base template that other templates extend.
    ├── admin.py                            # Configuration for the Django admin interface.
    ├── apps.py                             # Configuration for the students app.
    ├── forms.py                            # Forms for creating and updating Student and Marks models.
    ├── models.py                           # Contains the Student and Marks models.
    ├── test_views.py                       # Unit tests for the views in the students app.
    ├── urls.py                             # URL routing for the students app.
    └── views.py                            # View functions for handling student and marks management.

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.0.6 

### Installation
1. Clone the repository/Download project file
```
cd managementsystem
```
2. Create and Activate Virtual Environment
```
pip install vitualenv python -m venv env
source env/bin/ativate # On Windows use `env\Scripts\activate`
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. . Run migration
``` 
python manage.py migrate
```
5. Create Super User
```
python manage.py createsuperuser
```
6. Run the development server
```
python manage.py runserver
```
7. Open your browser and navigate to `http://localhost:8000/accounts/login/` to access the application.

### Usage

- Access the application at http://127.0.0.1:8000/
- Log in using the superuser credentials created earlier.
- Navigate through the application to manage students and their marks.

### Testing

Unit tests are provided to ensure the functionality of the application. To run the tests:

```
python manage.py test students
```
