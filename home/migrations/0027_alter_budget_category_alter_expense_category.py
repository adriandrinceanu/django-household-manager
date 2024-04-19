# Generated by Django 5.0.3 on 2024-04-19 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_message_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(choices=[('groceries', 'Groceries'), ('entertainment', 'Entertainment'), ('clothing', 'Clothing'), ('transportation', 'Transportation'), ('utilities', 'Utilities'), ('healthcare', 'Healthcare'), ('education', 'Education'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('groceries', 'Groceries'), ('entertainment', 'Entertainment'), ('clothing', 'Clothing'), ('transportation', 'Transportation'), ('utilities', 'Utilities'), ('healthcare', 'Healthcare'), ('education', 'Education'), ('other', 'Other')], max_length=50),
        ),
    ]
