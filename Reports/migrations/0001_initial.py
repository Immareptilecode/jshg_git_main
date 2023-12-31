# Generated by Django 2.0 on 2019-10-10 05:28

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Finance', '0004_auto_20190813_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_absence', to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_absence', to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Absence monthly account',
                'verbose_name_plural': 'Absence monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Cashfines_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_cashfines', to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_cashfines', to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Cash fine monthly account',
                'verbose_name_plural': 'Cash fine monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Exitfee_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_exitfee', to='Finance.charges_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_exitfee', to='Finance.charges_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Exit Fee monthly account',
                'verbose_name_plural': 'Exit Fee monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='LateReceipt_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='late_receipt_group', to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='late_receipt_individual', to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Late Receipt submission monthly account',
                'verbose_name_plural': 'Late Receipt submission  monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Loanfines_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Loan Fine monthly account',
                'verbose_name_plural': 'Loan Fine monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Loanform_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_loanform', to='Finance.charges_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_loanform', to='Finance.charges_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Loan Form monthly account',
                'verbose_name_plural': 'Loan Form monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='LoanInterest_fines_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Loan Interest fine monthly account',
                'verbose_name_plural': 'Loan Interest fine monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Loans_monthly_accounting_model',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('interest_on_loans_total', models.IntegerField(blank=True)),
                ('loans_outsanding_total', models.IntegerField(blank=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('group_payments', models.ManyToManyField(blank=True, related_name='group_loans_monthly', to='Finance.loan_repayment_register_group')),
                ('individual_payments', models.ManyToManyField(blank=True, related_name='individual_loans_monthly', to='Finance.loan_repayment_register_individual')),
            ],
            options={
                'verbose_name': 'Loan Monthly  account',
                'verbose_name_plural': 'Loan Monthly  accounts',
            },
        ),
        migrations.CreateModel(
            name='New_membership_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_membership', to='Finance.charges_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_membership', to='Finance.charges_payment_register_individual')),
            ],
            options={
                'verbose_name': 'New Membership monthly account',
                'verbose_name_plural': 'New Membership monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Office_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, to='Finance.charges_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, to='Finance.charges_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Office monthly account',
                'verbose_name_plural': 'Office monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='Shares_Noncontribution_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_noncontribution', to='Finance.fines_payment_register_group')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_noncontribution', to='Finance.fines_payment_register_individual')),
            ],
            options={
                'verbose_name': 'Shares non-contribution monthly account',
                'verbose_name_plural': 'Shares non-contribution monthly accounts',
            },
        ),
        migrations.CreateModel(
            name='SharesContribution_monthly_income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(blank=True)),
                ('total', models.IntegerField(blank=True)),
                ('group', models.ManyToManyField(blank=True, related_name='group_sharescontribution', to='Finance.gshare')),
                ('individual', models.ManyToManyField(blank=True, related_name='individual_sharescontribution', to='Finance.Share')),
            ],
            options={
                'verbose_name': 'Share Contribution',
                'verbose_name_plural': 'Share Contributions monthly accounts',
            },
        ),
    ]
