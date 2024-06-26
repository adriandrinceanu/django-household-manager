# Generated by Django 5.0.3 on 2024-04-11 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_budget_amount_alter_monthlybudget_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='year',
            field=models.PositiveIntegerField(blank=True, choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043)], default=2024, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='year',
            field=models.PositiveIntegerField(blank=True, choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043)], default=2024, null=True),
        ),
        migrations.AlterField(
            model_name='monthlybudget',
            name='year',
            field=models.PositiveIntegerField(blank=True, choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043)], default=2024, null=True),
        ),
    ]
