# Generated by Django 5.0.6 on 2024-07-21 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='score',
            field=models.FloatField(default=0.0),
        ),
    ]
