# Generated by Django 5.1.3 on 2024-12-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_project_api', '0016_alter_students_created_by_alter_students_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='created_on',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='deleted_on',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='modified_on',
            field=models.DateField(blank=True),
        ),
    ]
