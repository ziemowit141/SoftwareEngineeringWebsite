# Generated by Django 2.1.4 on 2019-01-12 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0003_auto_20190111_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='academic_degree',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_reviewer',
            field=models.BooleanField(default=True),
        ),
    ]
