# Generated by Django 3.2.8 on 2021-11-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lessons_lesson_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]