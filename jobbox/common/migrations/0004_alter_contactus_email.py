# Generated by Django 4.2.3 on 2023-07-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
