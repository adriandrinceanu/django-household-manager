# Generated by Django 5.0.3 on 2024-04-19 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_budget_category_alter_expense_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='deadline',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
