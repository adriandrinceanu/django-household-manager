# Generated by Django 5.0.3 on 2024-04-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_member_cover_pic_alter_member_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic'),
        ),
    ]
