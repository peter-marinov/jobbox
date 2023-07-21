# Generated by Django 4.2.3 on 2023-07-20 16:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('company_logo', models.ImageField(upload_to='companies_logo/')),
                ('programming_language', models.CharField(max_length=15)),
                ('salary', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(20), django.core.validators.MaxLengthValidator(300)])),
                ('hr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
