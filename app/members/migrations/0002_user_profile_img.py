# Generated by Django 2.1.2 on 2018-10-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default=0, upload_to='user'),
            preserve_default=False,
        ),
    ]
