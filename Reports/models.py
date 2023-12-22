from django.db import models
from Finance.models import fines_payment_register_individual, charges_payment_register_individual, fines_payment_register_group, charges_payment_register_group, Share, gshare, loan_repayment_register_individual, loan_repayment_register_group
from Finance.models import IndividualDisbursed_Loan, GroupDisbursed_Loan
from django.utils import timezone
import uuid
# Create your models here.
from .models import *
from Membership.models import Member, Groups

#fines and charges accounting models

class Loanfines_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True)
	group=models.ManyToManyField(fines_payment_register_group, blank=True)
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	def model_name(self):
		return ["Loan Fine"]

	class Meta:
		verbose_name="Loan Fine monthly account"
		verbose_name_plural = 'Loan Fine monthly accounts'
	
class LoanInterest_fines_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True)
	group=models.ManyToManyField(fines_payment_register_group, blank=True)
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	def model_name(self):
		return ["Interest Fine"]

	class Meta:
		verbose_name="Loan Interest fine monthly account"
		verbose_name_plural = 'Loan Interest fine monthly accounts'

class Absence_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True, related_name='individual_absence')
	group=models.ManyToManyField(fines_payment_register_group, blank=True, related_name='group_absence')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)
	
	def model_name(self):
		return ["Absentism"]

	class Meta:
		verbose_name="Absence monthly account"
		verbose_name_plural = 'Absence monthly accounts'

	
	

class Cashfines_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True, related_name='individual_cashfines')
	group=models.ManyToManyField(fines_payment_register_group, blank=True, related_name='group_cashfines')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Cash fine monthly account"
		verbose_name_plural = 'Cash fine monthly accounts'

	def model_name(self):
		return ["Cashfines"]
	

class Loanform_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(charges_payment_register_individual, blank=True, related_name='individual_loanform')
	group=models.ManyToManyField(charges_payment_register_group, blank=True, related_name='group_loanform')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Loan Form monthly account"
		verbose_name_plural = 'Loan Form monthly accounts'

	def model_name(self):
		return ["loan form"]
	
class Exitfee_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(charges_payment_register_individual, blank=True, related_name='individual_exitfee')
	group=models.ManyToManyField(charges_payment_register_group, blank=True, related_name='group_exitfee')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Exit Fee monthly account"
		verbose_name_plural = 'Exit Fee monthly accounts'	

	def model_name(self):
		return ["exitfee"]
	
	
class New_membership_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(charges_payment_register_individual, blank=True, related_name='individual_membership')
	group=models.ManyToManyField(charges_payment_register_group, blank=True, related_name='group_membership')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="New Membership monthly account"
		verbose_name_plural = 'New Membership monthly accounts'

	def model_name(self):
		return ["newMembership"]
	
class Office_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(charges_payment_register_individual, blank=True)
	group=models.ManyToManyField(charges_payment_register_group, blank=True)
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Office monthly account"
		verbose_name_plural = 'Office monthly accounts'

	def model_name(self):
		return ["office"]
	


class Shares_Noncontribution_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True, related_name='individual_noncontribution')
	group=models.ManyToManyField(fines_payment_register_group, blank=True, related_name='group_noncontribution')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Shares non-contribution monthly account"
		verbose_name_plural = 'Shares non-contribution monthly accounts'

	def model_name(self):
		return ["non contribution"]
	

class LateReceipt_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(fines_payment_register_individual, blank=True, related_name='late_receipt_individual')
	group=models.ManyToManyField(fines_payment_register_group, blank=True, related_name='late_receipt_group')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Late Receipt submission monthly account"
		verbose_name_plural = 'Late Receipt submission  monthly accounts'

	def model_name(self):
		return ["lateReceipt"]
	

# shares contributions


class SharesContribution_monthly_income(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	individual=models.ManyToManyField(Share, blank=True, related_name='individual_sharescontribution')
	group=models.ManyToManyField(gshare, blank=True, related_name='group_sharescontribution')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)
	total=models.IntegerField(blank=True)

	class Meta:
		verbose_name="Share Contribution"
		verbose_name_plural = 'Share Contributions monthly accounts'


#loans_accounting model
class Loans_monthly_accounting_model(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	interest_on_loans_total=models.IntegerField(blank=True)
	loans_outsanding_total=models.IntegerField(blank=True)
	group_payments=models.ManyToManyField(loan_repayment_register_group, blank=True, related_name='group_loans_monthly')
	individual_payments=models.ManyToManyField(loan_repayment_register_individual, blank=True, related_name='individual_loans_monthly')
	start=models.DateField(default=timezone.now)
	end=models.DateField(blank=True)

	class Meta:
		verbose_name="Loan Monthly  account"
		verbose_name_plural = 'Loan Monthly  accounts'


class Share_Capital_deductions_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=False)
	individual=models.ForeignKey(Member, on_delete=models.CASCADE, blank=False)
	date=models.DateField(default=timezone.now)
	class Meta:
		verbose_name="Share Capital individual"
		verbose_name_plural = 'Share Capital individuals'

class Share_Capital_deductions_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Amount=models.IntegerField(blank=False)
	group=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=False)
	date=models.DateField(default=timezone.now)

	class Meta:
		verbose_name="Share Capital group"
		verbose_name_plural = 'Share Capital groups'

class Loanoffset_deductions_group(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	balance_amount=models.FloatField(blank=False)
	loan=models.ForeignKey(GroupDisbursed_Loan, on_delete=models.CASCADE, blank=False)
	date=models.DateField(default=timezone.now)

	class Meta:
		verbose_name="Loan offset group"
		verbose_name_plural = 'Loan offset groups'

class Loanoffset_deductions_individual(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	balance_amount=models.FloatField(blank=False)
	loan=models.ForeignKey(IndividualDisbursed_Loan, on_delete=models.CASCADE, blank=False)
	date=models.DateField(default=timezone.now)

	class Meta:
		verbose_name="Loan offset individual"
		verbose_name_plural = 'Loan offset individuals'	
		
