# Generated by Django 5.0.6 on 2024-07-21 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_student_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_class',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')]),
        ),
    ]
