# Generated by Django 2.1.8 on 2020-05-13 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20200513_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='desc',
            field=models.CharField(default='', max_length=200, verbose_name='描述'),
        ),
    ]
