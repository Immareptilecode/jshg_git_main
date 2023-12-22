from rest_framework import serializers
from .models import Share, gshare, IndividualDisbursed_Loan, GroupDisbursed_Loan, loan_repayment_register_individual, loan_repayment_register_group
from Membership.models import Member
from Reports.models import Share_Capital_deductions_individual, Share_Capital_deductions_group
class ShareSerializer(serializers.ModelSerializer):
	class Meta:
		model = Share
		fields = '__all__'

class ShareCapitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Share_Capital_deductions_individual
		fields = '__all__'

class GroupShareCapitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Share_Capital_deductions_group
		fields = '__all__'

class GroupShareSerializer(serializers.ModelSerializer):
	class Meta:
		model = gshare
		fields = '__all__'


class individual_loanSerializer(serializers.ModelSerializer):
	gurantor=serializers.PrimaryKeyRelatedField(many=True, allow_empty=False, queryset=Member.objects.all())
	class Meta:
		model = IndividualDisbursed_Loan
		fields = ('installments', 'gurantor', 'Borrower', 'Amount', 'Date_disbursment')

		


class group_loanSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupDisbursed_Loan
		fields = '__all__'

class individual_registerSerializer(serializers.ModelSerializer):
	class Meta:
		model = loan_repayment_register_individual
		fields = '__all__'

		

class group_registerSerializer(serializers.ModelSerializer):
	class Meta:
		model = loan_repayment_register_group
		fields = '__all__'


#debts

from .models import charges_record_individual, charges_record_group, fines_record_individual, fines_record_group
class charge_indi_acc(serializers.ModelSerializer):
	class Meta:
		model = charges_record_individual
		fields = ('member', 'Amount_due', 'Date', 'Particulars')

class charge_group_acc(serializers.ModelSerializer):
	class Meta:
		model = charges_record_group
		fields = '__all__'

class fine_group_acc(serializers.ModelSerializer):
	class Meta:
		model = fines_record_group
		fields = '__all__'

class fine_indi_acc(serializers.ModelSerializer):
	class Meta:
		model = fines_record_individual
		fields = '__all__'