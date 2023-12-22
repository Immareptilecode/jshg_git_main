from django.contrib import admin
from .models import IndividualDisbursed_Loan, loan_repayment_register_individual, Loan_repayment_refrence, GroupDisbursed_Loan, loan_repayment_register_group
from .models import Share, charges_record_individual, fines_record_individual, fines_record_group, charges_payment_register_individual, charges_record_group, fines_payment_register_individual, fines_payment_register_group,  charges_payment_register_group
# Register your models here.


class sharesAdmin(admin.ModelAdmin):
	
	list_display =('first_name', 'Amount', 'membership_no', 'date_of_payment')
	def first_name(self, request):

		return request.member.first_name
	def membership_no(self, request):
		return request.member.membership_no

	def date_of_payment(self, request):
		return request.date_payment

class Fines_individualAdmin(admin.ModelAdmin):
	
	list_display =('member','Particulars','Amount_due', 'Date', 'paid')


		
class Fines_groupAdmin(admin.ModelAdmin):
	
	list_display =('group','Particulars','Amount_due', 'Date', 'paid')





class Fines_group_paymentAdmin(admin.ModelAdmin):
	
	list_display =('Amount', 'date_payment', 'particular_fine')

class Fines_individual_paymentAdmin(admin.ModelAdmin):
	
	list_display =('Amount', 'date_payment', 'particular_fine')
	


	


class Charges_individual_paymentAdmin(admin.ModelAdmin):
	
	list_display =('Amount', 'date_payment', 'particular_charge')

class Charges_group_paymentAdmin(admin.ModelAdmin):
	
	list_display =('Amount', 'date_payment', 'particular_charge')


admin.site.register(IndividualDisbursed_Loan)


admin.site.register(fines_record_individual, Fines_individualAdmin)
admin.site.register(fines_record_group, Fines_groupAdmin)

admin.site.register(charges_record_individual, Fines_individualAdmin)
admin.site.register(charges_record_group, Fines_groupAdmin)


admin.site.register(fines_payment_register_individual, Fines_individual_paymentAdmin)
admin.site.register(fines_payment_register_group, Fines_group_paymentAdmin)

admin.site.register(charges_payment_register_individual, Charges_individual_paymentAdmin)
admin.site.register(charges_payment_register_group, Charges_group_paymentAdmin)

admin.site.register(GroupDisbursed_Loan)

admin.site.register(loan_repayment_register_individual)
admin.site.register(loan_repayment_register_group)


admin.site.register(Share, sharesAdmin)


