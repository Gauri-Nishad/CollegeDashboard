# Generated by Django 5.1.3 on 2024-12-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_project_api', '0029_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='img/'),
        ),
    ]
