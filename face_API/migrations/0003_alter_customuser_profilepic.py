# Generated by Django 3.2 on 2021-05-07 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_API', '0002_alter_customuser_userfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profilePic',
            field=models.ImageField(upload_to='face_API/static/face_API/img/uploads'),
        ),
    ]
