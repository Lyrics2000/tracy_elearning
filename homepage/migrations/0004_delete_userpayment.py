# Generated by Django 3.2.8 on 2022-01-05 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_userpayment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPayment',
        ),
    ]