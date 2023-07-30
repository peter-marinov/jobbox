# Generated by Django 4.2.3 on 2023-07-29 10:32

from django.db import migrations, models
import jobbox.job.validators


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_alter_uploadcv_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company_logo',
            field=models.ImageField(upload_to='companies_logo', validators=[jobbox.job.validators.FileSizeValidatorInMB(1)]),
        ),
    ]