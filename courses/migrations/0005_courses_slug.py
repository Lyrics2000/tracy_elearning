# Generated by Django 3.2.8 on 2021-11-21 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lessonassignmentfiles_lessonfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
