from django.db import models
from Membership.models import Member, Groups
from django.utils import timezone
from datetime import timedelta
import uuid
from django.db.models import DO_NOTHING
# Create your models here.
OFFENCES_CHOICES= (
('non contribution', 'non_contribution'),
('Loan Fine', 'loan_fine'),
('Interest Fine', 'interest_fine'),
('Absentism', 'absentism'),
('Cashfines', "cash_fine"),
('lateReceipt', 'late_receipt'),

)

CHARGES_CHOICES= (
('loan form', 'loan_form'),
('office', 'office_fee'),
('exitfee', 'exit_fee'),
('newMembership', 'new_membership'),


)


CHARGES_CHOICES_GROUP= (
('loan form', 'loan_form'),
('office', 'office_fee'),
('exitfee', 'exit_fee'),
('newMembership', 'new_membership'),

)

class Share(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	member=models.ForeignKey(Member, on_delete=models.CASCADE, blank=False)
	Amount= models.IntegerField(blank=False)
	date_payment=models.DateField(blank=False, default=timezone.now)

	def __str__(self):
		template=' Shares payment of Amount: {0.Amount} made on {0.date_payment} by {0.member}'
		return template.format(self)

class gshare(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	group=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=False)
	Amount= models.IntegerField(blank=False)
	date_payment=models.DateField(blank=False, default=timezone.now)

	def __str__(self):
		template=' Shares payment of Amount: {0.Amount} made on {0.date_payment} by {0.group}'
		return template.format(self)


class Loan_repayment_refrence(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	min_amount=models.IntegerField()
	max_amount=models.IntegerField()
	repayment_period=models.IntegerField(verbose_name='Repayment Period in Months')
	def __str__(self):
		template= 'min {0.min_amount}   max {0.max_amount}'
		return template.format(self)



class IndividualDisbursed_Loan(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Date_disbursment=models.DateField(blank=False)
	Amount=models.IntegerField(blank=False)
	Borrower=models.ForeignKey(Member, on_delete=models.CASCADE, blank=False)
	gurantor=models.ManyToManyField(Member, blank=True, related_name='Gurantors_individual_loan')
	installments=models.IntegerField(verbose_name='Repayment Period in Months', default=12, blank=True)
	re_paid=models.BooleanField(default=False)

	def __str__(self):
		template= '{0.Borrower} amount {0.Amount} date {0.Date_disbursment}'
		return template.format(self)



class GroupDisbursed_Loan(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Date_disbursment=models.DateField(blank=False)
	Amount=models.IntegerField(blank=False)
	Borrower=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=False)
	gurantor=models.ManyToManyField(Member, blank=False, related_name='Gurantors_group_loan')
	installments=models.IntegerField(verbose_name='Repayment Period in Months', default=12, blank=True)
	date_last_principal=models.DateField(blank=True, editable=False)
	re_paid=models.BooleanField(default=False)

	def __str__(self):
		template= '{0.Borrower} amount {0.Amount} date {0.Date_disbursment}'
		return template.format(self)

			
		
class loan_repayment_register_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	loan=models.ForeignKey(IndividualDisbursed_Loan, on_delete=models.CASCADE, blank=False, default=uuid.uuid4)
	Amount=models.IntegerField(blank=False)
	date_payment=models.DateField(blank=False)

	def __str__(self):
		template = 'loan payment , Amount: {0.Amount} paid on:  {0.date_payment} '
		return template.format(self)

class loan_repayment_register_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	loan=models.ForeignKey(GroupDisbursed_Loan, on_delete=models.CASCADE, blank=False, default=uuid.uuid4)
	Amount=models.IntegerField(blank=False)
	date_payment=models.DateField(blank=False, default=timezone.now)

	def __str__(self):
		template = 'loan payment , Amount: {0.Amount} paid on:  {0.date_payment} '
		return template.format(self)

# clarify rules to jiendeleze so they can decide based on the optimum delete procedures for a customers debts


class charges_record_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	member=models.ForeignKey(Member, on_delete=models.CASCADE, blank=False, default=uuid.uuid4)
	Amount_due=models.IntegerField(blank=True)
	Date=models.DateField(default=timezone.now) 
	Particulars=models.CharField(max_length=30, choices=CHARGES_CHOICES)
	paid=models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Individual charges Record'
		verbose_name_plural = 'Individual charges Records'

class charges_record_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	group=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=False, default=uuid.uuid4)
	Amount_due=models.IntegerField(blank=True)
	Date=models.DateField(default=timezone.now) 
	Particulars=models.CharField(max_length=30, choices=CHARGES_CHOICES_GROUP)
	paid=models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Group charges Record'
		verbose_name_plural = 'Group charges Records'


class fines_record_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	member=models.ForeignKey(Member, on_delete=models.CASCADE, blank=False, default=uuid.uuid4)
	Amount_due=models.IntegerField(blank=True)
	Date=models.DateField(default=timezone.now) 
	Particulars=models.CharField(max_length=30, choices=OFFENCES_CHOICES)	
	paid=models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Individual fines Record'
		verbose_name_plural = 'Individual fines Records'

class fines_record_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	group=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=True, default=uuid.uuid4)
	Amount_due=models.IntegerField(blank=True)
	Date=models.DateField(default=timezone.now) 
	Particulars=models.CharField(max_length=30, choices=OFFENCES_CHOICES)	
	paid=models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Group Fines Record'
		verbose_name_plural = 'Group Fines Records'


# charges and fines payment registers for both individual's and groups
class fines_payment_register_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=True)
	fine=models.ManyToManyField(fines_record_individual, blank=False, related_query_name="fines")
	date_payment=models.DateField(default=timezone.now)

	class Meta:
		verbose_name = 'Individual Fines Payment Register'
		verbose_name_plural = 'Individual Fines Payment Register'

	def __str__(self):
		pc=self.particular_fine()
		template='%s payment of amount: {0.Amount} made on date {0.date_payment}' % pc
		return template.format(self)

	def particular_fine(self):
		#print(self.fine.all())
		try:
			return self.fine.all()[0].Particulars
		except IndexError:
			return " no fine"


class charges_payment_register_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=True)
	charge=models.ManyToManyField(charges_record_individual, blank=False, null=False)
	date_payment=models.DateField(default=timezone.now)

	def __str__(self):
		pc=self.particular_charge()
		template='%s payment of amount: {0.Amount} made on date {0.date_payment}' % pc
		return template.format(self)

	def particular_charge(self):
		try:
			parts=[]
			for i in self.charge.all():
				parts.append((i.Particulars, i.Amount_due))
				
			return parts

		except IndexError:
			return " no charge"
		

	class Meta:
		verbose_name = 'Individual Charges Payment Register'
		verbose_name_plural = 'Individual Charges Payment Register'

class fines_payment_register_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=True)
	fine=models.ManyToManyField(fines_record_group, blank=False)
	date_payment=models.DateField(default=timezone.now)

	def __str__(self):
		pc=self.particular_fine()
		template='%s payment of amount: {0.Amount} made on date {0.date_payment}' % pc
		return template.format(self)

	def particular_fine(self):
		try:
			return self.fine.all()[0].Particulars

		except IndexError:
			return " no fine"
	class Meta:
		verbose_name = 'Group Fines Payment Register'
		verbose_name_plural = 'Group Fines Payment Register'

class charges_payment_register_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=True)
	charge=models.ManyToManyField(charges_record_group, blank=False)
	date_payment=models.DateField(default=timezone.now)

	def __str__(self):
		pc=self.particular_charge()
		template='%s payment of amount: {0.Amount} made on date {0.date_payment}' % pc
		return template.format(self)

	def particular_charge(self):
		try:
			return self.charge.all()[0].Particulars

		except IndexError:
			return " no charge"
	
	class Meta:
		verbose_name = 'Group Charges Payment Register'
		verbose_name_plural = 'Group Charges Payment Register'

