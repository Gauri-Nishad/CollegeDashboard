# Generated by Django 5.1.3 on 2024-12-06 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college_project_api', '0018_remove_faculties_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='user',
        ),
    ]
