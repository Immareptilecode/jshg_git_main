# Generated by Django 2.2.9 on 2020-05-08 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reports', '0002_loanoffset_deductions_group_loanoffset_deductions_individual_share_capital_deductions_group_share_ca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanoffset_deductions_group',
            name='balance_amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='loanoffset_deductions_individual',
            name='balance_amount',
            field=models.FloatField(),
        ),
    ]
