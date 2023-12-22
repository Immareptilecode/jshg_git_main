from .models import IndividualDisbursed_Loan, GroupDisbursed_Loan, charges_payment_register_individual, fines_payment_register_individual, charges_record_individual
from django import forms
#group related models
from .models import fines_record_group, fines_payment_register_group, charges_payment_register_group, charges_record_group
from Reports.models import Loanoffset_deductions_group, Loanoffset_deductions_individual
class individual_loan_form(forms.ModelForm):
	
	class Meta:
		model=IndividualDisbursed_Loan
		fields = ('installments', 'Borrower', 'Amount', 'Date_disbursment')


class group_loan_form(forms.ModelForm):
	
	class Meta:
		model=GroupDisbursed_Loan
		fields = ('installments', 'Borrower', 'Amount', 'Date_disbursment')



class individual_loan_offset(forms.ModelForm):
	
	class Meta:
		model=Loanoffset_deductions_individual
		fields = ('loan', 'balance_amount', 'date')


class group_loan_offset(forms.ModelForm):
	
	class Meta:
		model=Loanoffset_deductions_group
		fields = ('loan', 'balance_amount', 'date')



class individual_charges_payment_form(forms.ModelForm):

	class Meta:
		model=charges_payment_register_individual
		fields = ('Amount', 'date_payment')

class group_charges_payment_form(forms.ModelForm):

	class Meta:
		model=charges_payment_register_group
		fields = ('Amount', 'date_payment')

class individual_fines_payment_form(forms.ModelForm):

	class Meta:
		model=fines_payment_register_individual
		fields = ('Amount', 'date_payment')

class group_fines_payment_form(forms.ModelForm):

	class Meta:
		model=fines_payment_register_group
		fields = ('Amount', 'date_payment')



class individual_charges_record_form(forms.ModelForm):

	class Meta:
		model=charges_record_individual
		fields = ('member', 'Amount_due', 'Date', 'Particulars')

class group_charges_record_form(forms.ModelForm):

	class Meta:
		model=charges_record_group
		fields = ('group', 'Amount_due', 'Date', 'Particulars')