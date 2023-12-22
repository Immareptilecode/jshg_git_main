from django.contrib import admin

from .models import LoanInterest_fines_monthly_income, Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income, Shares_Noncontribution_monthly_income, SharesContribution_monthly_income, Loans_monthly_accounting_model, LateReceipt_monthly_income, Share_Capital_deductions_individual, Share_Capital_deductions_group, Loanoffset_deductions_individual, Loanoffset_deductions_group





# Register your models here.
class sharecapital_individualsAdmin(admin.ModelAdmin):
	
	list_display =('individual','Amount','date')



admin.site.register(LoanInterest_fines_monthly_income)
admin.site.register(Loanfines_monthly_income)
admin.site.register(Absence_monthly_income)
admin.site.register(Cashfines_monthly_income)
admin.site.register(Loanform_monthly_income)
admin.site.register(Exitfee_monthly_income)
admin.site.register(New_membership_monthly_income)
admin.site.register(Office_monthly_income)

admin.site.register(Shares_Noncontribution_monthly_income)
admin.site.register(SharesContribution_monthly_income)
admin.site.register(Loans_monthly_accounting_model)
admin.site.register(LateReceipt_monthly_income)
admin.site.register(Share_Capital_deductions_individual, sharecapital_individualsAdmin)
admin.site.register(Share_Capital_deductions_group)
admin.site.register(Loanoffset_deductions_individual)
admin.site.register(Loanoffset_deductions_group)


