# Generated by Django 5.0.3 on 2024-04-19 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_unreadmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unreadmessage',
            name='user',
        ),
        migrations.AddField(
            model_name='unreadmessage',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.member'),
        ),
    ]
