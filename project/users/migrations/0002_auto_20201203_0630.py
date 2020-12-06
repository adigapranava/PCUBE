# Generated by Django 3.1.2 on 2020-12-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fullname',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phoneno',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
