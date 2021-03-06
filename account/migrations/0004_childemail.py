# Generated by Django 3.2.8 on 2021-12-07 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_pic_image_filled'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_email', models.EmailField(max_length=254)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
