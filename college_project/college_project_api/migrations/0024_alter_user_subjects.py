# Generated by Django 5.1.3 on 2024-12-15 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_project_api', '0023_alter_students_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(null=True, related_name='subjects', to='college_project_api.subjects'),
        ),
    ]
