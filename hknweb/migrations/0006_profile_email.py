# Generated by Django 2.1.5 on 2019-02-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hknweb', '0005_delete_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]