# Generated by Django 3.2.8 on 2021-11-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_lessons_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='lesson_body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
