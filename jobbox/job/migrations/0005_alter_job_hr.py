# Generated by Django 4.2.3 on 2023-07-21 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0004_alter_job_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='hr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
