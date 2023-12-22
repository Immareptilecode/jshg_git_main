# Generated by Django 2.0 on 2019-08-13 10:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Membership', '0003_groups_extra_details'),
        ('Finance', '0003_auto_20190813_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='charges_payment_register_group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount', models.IntegerField(blank=True)),
                ('date_payment', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Group Charges Payment Register',
                'verbose_name_plural': 'Group Charges Payment Register',
            },
        ),
        migrations.CreateModel(
            name='charges_payment_register_individual',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount', models.IntegerField(blank=True)),
                ('date_payment', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Individual Charges Payment Register',
                'verbose_name_plural': 'Individual Charges Payment Register',
            },
        ),
        migrations.CreateModel(
            name='charges_record_group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount_due', models.IntegerField(blank=True)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Particulars', models.CharField(choices=[('loan form', 'loan_form'), ('office', 'office_fee'), ('exitfee', 'exit_fee')], max_length=30)),
                ('paid', models.BooleanField(default=False)),
                ('group', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.DO_NOTHING, to='Membership.Groups')),
            ],
            options={
                'verbose_name': 'Group charges Record',
                'verbose_name_plural': 'Group charges Records',
            },
        ),
        migrations.CreateModel(
            name='charges_record_individual',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount_due', models.IntegerField(blank=True)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Particulars', models.CharField(choices=[('loan form', 'loan_form'), ('office', 'office_fee'), ('exitfee', 'exit_fee')], max_length=30)),
                ('paid', models.BooleanField(default=False)),
                ('member', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.DO_NOTHING, to='Membership.Member')),
            ],
            options={
                'verbose_name': 'Individual charges Record',
                'verbose_name_plural': 'Individual charges Records',
            },
        ),
        migrations.CreateModel(
            name='fines_payment_register_group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount', models.IntegerField(blank=True)),
                ('date_payment', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Group Fines Payment Register',
                'verbose_name_plural': 'Group Fines Payment Register',
            },
        ),
        migrations.CreateModel(
            name='fines_payment_register_individual',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount', models.IntegerField(blank=True)),
                ('date_payment', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Individual Fines Payment Register',
                'verbose_name_plural': 'Individual Fines Payment Register',
            },
        ),
        migrations.CreateModel(
            name='fines_record_group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount_due', models.IntegerField(blank=True)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Particulars', models.CharField(choices=[('Shares non contribution', 'non_contribution'), ('Falirue to pay monthly loan principal', 'principal_latness'), ('Absentism', 'absentism')], max_length=30)),
                ('paid', models.BooleanField(default=False)),
                ('group', models.ForeignKey(blank=True, default=uuid.uuid4, on_delete=django.db.models.deletion.DO_NOTHING, to='Membership.Groups')),
            ],
            options={
                'verbose_name': 'Group Fines Record',
                'verbose_name_plural': 'Group Fines Records',
            },
        ),
        migrations.CreateModel(
            name='fines_record_individual',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Amount_due', models.IntegerField(blank=True)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Particulars', models.CharField(choices=[('Shares non contribution', 'non_contribution'), ('Falirue to pay monthly loan principal', 'principal_latness'), ('Absentism', 'absentism')], max_length=30)),
                ('paid', models.BooleanField(default=False)),
                ('member', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.DO_NOTHING, to='Membership.Member')),
            ],
            options={
                'verbose_name': 'Individual fines Record',
                'verbose_name_plural': 'Individual fines Records',
            },
        ),
        migrations.DeleteModel(
            name='Charges_refrence',
        ),
        migrations.DeleteModel(
            name='fines_refrence',
        ),
        migrations.AlterField(
            model_name='loan_repayment_register_group',
            name='loan',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='Finance.GroupDisbursed_Loan'),
        ),
        migrations.AlterField(
            model_name='loan_repayment_register_individual',
            name='loan',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='Finance.IndividualDisbursed_Loan'),
        ),
        migrations.AddField(
            model_name='fines_payment_register_individual',
            name='fine',
            field=models.ManyToManyField(to='Finance.fines_record_individual'),
        ),
        migrations.AddField(
            model_name='fines_payment_register_group',
            name='fine',
            field=models.ManyToManyField(to='Finance.fines_record_group'),
        ),
        migrations.AddField(
            model_name='charges_payment_register_individual',
            name='charge',
            field=models.ManyToManyField(to='Finance.charges_record_individual'),
        ),
        migrations.AddField(
            model_name='charges_payment_register_group',
            name='charge',
            field=models.ManyToManyField(to='Finance.charges_record_group'),
        ),
    ]
