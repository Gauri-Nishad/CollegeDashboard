# Generated by Django 5.1.3 on 2024-12-26 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_project_api', '0034_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
