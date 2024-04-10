# Generated by Django 5.0.3 on 2024-04-09 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_budget_month_budget_year_expense_month_expense_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='family',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='month',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='year',
        ),
        migrations.CreateModel(
            name='MonthlyBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('month', models.CharField(blank=True, choices=[('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apr', 'April'), ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'), ('sep', 'September'), ('oct', 'October'), ('nov', 'November'), ('dec', 'December')], max_length=3, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_budgets', to='home.family')),
            ],
        ),
        migrations.AddField(
            model_name='budget',
            name='monthly_budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='home.monthlybudget'),
        ),
    ]