# Generated by Django 3.2.8 on 2022-01-05 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0011_lessons_paid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaResquest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchantRequestid', models.CharField(max_length=255)),
                ('chechoutrequestid', models.CharField(max_length=255)),
                ('responsecode', models.CharField(max_length=10)),
                ('responsedescription', models.TextField()),
                ('customerMessage', models.TextField()),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('request_id', models.CharField(blank=True, max_length=255, null=True)),
                ('callback_url', models.URLField(blank=True, null=True)),
                ('lesson_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lessons')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MpesaQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_code', models.CharField(max_length=255)),
                ('response_description', models.TextField()),
                ('merchant_id', models.CharField(max_length=255)),
                ('checkout_request_id', models.CharField(max_length=255)),
                ('result_code', models.CharField(max_length=255)),
                ('result_description', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('request_id', models.TextField()),
                ('mpesa_request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.mpesaresquest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
