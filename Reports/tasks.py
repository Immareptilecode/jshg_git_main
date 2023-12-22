from background_task import background
from .models import Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income, Interest_monthly_income, Shares_Noncontribution_monthly_income, LoanInterest_fines_monthly_income, SharesContribution_monthly_income, Loans_monthly_accounting_model

from Finance.models import fines_payment_register_individual, charges_payment_register_individual, fines_payment_register_group, charges_payment_register_group, Share, gshare

from datetime import datetime
from datetime import timedelta
import calendar


all_monthly_models=[SharesContribution_monthly_income, Loans_monthly_accounting_model, LoanInterest_fines_monthly_income, Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income, Interest_monthly_income, Shares_Noncontribution_monthly_income]
daily_model_guide={"charges":[Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income], 'fines':[LoanInterest_fines_monthly_income, Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Shares_Noncontribution_monthly_income]}
class MonthlyTasks(object):
	"""docstring for MonthlyTasks"""
	def __init__(self):
		super(MonthlyTasks, self).__init__()
		
	def  Add_new_entrys(self):
		"""
		This guys job is to simply add new enties for all monthly accounting models	
		
		"""
		for i in all_monthly_models:

			new_entry=i()
			new_entry.save()


	def check_if_month_is_done(self):
		today=datetime.now()
		current_month_days=calendar.monthrange(today.year, today.month)[1]
		return current_month_days == today.day 


	def record_enddate(self):
		all_ending_entries=self.fetch_all_current_entries()
		for i in all_ending_entries:
			i.end = datetime.now().date()
	#def get_current_entry(self):




class DebtsDailyTasks(object):
	"""docstring for DebtsDailyTasks"""
	def __init__(self):
		super(DebtsDailyTasks, self).__init__()
		self.today=datetime.now()
	def fetch_current_entry(self, model):

		entries=model.objects.all().order_by("-start") 
		
		try:

			return entries[0]  
		except IndexError:
			#this would mean that this is a completely new accounting model with no entries at all

			new_entry=model()
			new_entry.save()
			#so we create a new one 

			#then return it
			return new_entry


	def fetch_added_payments(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		return (individuals, groups )



	def fetch_this_months_payments_fines(self, random_accounting_model_entry):
			today_payments_individual=[] #any new payments made today
			today_payments_group=[]	#any new payments made today
			today=self.today
			groups=fines_payment_register_group.objects.all().filter(fine__Particulars__in = random_accounting_model_entry.model_name())
			individual=fines_payment_register_individual.objects.all().filter(fine__Particulars__in = random_accounting_model_entry.model_name())

			for i in individual:

				if i.date_payment.month == today.month and i.date_payment.year == today.year:
					today_payments_individual.append(i)

			for i in groups:
				if i.date_payment.month == today.month and i.date_payment.year == today.year:
					today_payments_group.append(i)
			return(today_payments_individual, today_payments_group)

	def fetch_this_months_payments_charges(self, random_accounting_model_entry):
			today_payments_individual=[] #any new payments made today
			today_payments_group=[]	#any new payments made today
			today=self.today
			groups=charges_payment_register_group.objects.all().filter(charge__Particulars__in = random_accounting_model_entry.model_name())
			individual=charges_payment_register_individual.objects.all().filter(charge__Particulars__in = random_accounting_model_entry.model_name())

			for i in individual:
				if i.date_payment.month == today.month and i.date_payment.year == today.year:
					today_payments_individual.append(i)

			for i in groups:
				if i.date_payment.month == today.month and i.date_payment.year == today.year:
					today_payments_group.append(i)
			return(today_payments_individual, today_payments_group)


	def collect_fines_payments(self):
		
		for model in daily_model_guide['fines']:
			#this is the loop of all accounting models

			current_entry=self.fetch_current_entry(model)
			recorded_payments=self.fetch_added_payments(current_entry)

			#payments

			this_months_fine_payments=self.fetch_this_months_payments_fines(current_entry) #Specific to this model

			for i in this_months_fine_payments[0]:
				if i not in recorded_payments[0]:

					current_entry.individual.add(i.pk)
					print('Successfully collected individual fine payment(s): %s'% i)
				else:
					print('No collected individual fine payments')



			for i in this_months_fine_payments[1]:
				if i not in recorded_payments[1]:
					current_entry.group.add(i.pk)
					print('successfully collected group fine payment(s): %s'% i)
				else:
					print('No collected group fine payments')


	def collect_charges_payments(self):
		
		for model in daily_model_guide['charges']:
			#this is the loop of all accounting models

			current_entry=self.fetch_current_entry(model)
			recorded_payments=self.fetch_added_payments(current_entry)

			#payments

			todays_payments=self.fetch_this_months_payments_charges(current_entry) #Specific to this model

			for i in todays_payments[0]:
				if i not in recorded_payments[0]:

					current_entry.individual.add(i.pk)
					print('Successfully collected individual charges payment(s): %s'% i)
				else:
					print('No collected individual charges payments')



			for i in todays_payments[1]:
				if i not in recorded_payments[1]:
					current_entry.group.add(i.pk)
					print('successfully collected group charges payment(s): %s'% i)
				else:
					print('No collected group charges payments')
			
			#print(current_entry.individual.all(), 'individual')
	#def collect_shares_payments(self):



	def calculate_totals(self):

		for model in daily_model_guide['fines']:
			current_entry=self.fetch_current_entry(model)
			recorded_payments=self.fetch_added_payments(current_entry)
			total=0
			for i in recorded_payments[0]:
				total +=i.Amount


			for i in recorded_payments[1]:
				total +=i.Amount

			current_entry.total=total
			current_entry.save()

		for model in daily_model_guide['charges']:
			current_entry=self.fetch_current_entry(model)
			recorded_payments=self.fetch_added_payments(current_entry)
			total=0
			for i in recorded_payments[0]:
				total +=i.Amount


			for i in recorded_payments[1]:
				total +=i.Amount

			current_entry.total=total
			current_entry.save()












class SharesDailyTasks(object):
	"""docstring for SharesDailyTasks"""
	def __init__(self):
		super(SharesDailyTasks, self).__init__()

	def fetch_current_entry(self):
		entries=SharesContribution_monthly_income.objects.all().order_by("-start") 
		
		try:

			return entries[0]  
		except IndexError:
			new_entry=SharesContribution_monthly_income()
			new_entry.save()

			return new_entry

	def fetch_this_months_payments(self):
		group_shares=gshare.objects.all()
		individual_shares=Share.objects.all()
		today=datetime.now()
		today_group=[]
		today_individual=[]

		for i in group_shares:
			if i.date_payment.month == today.month and i.date_payment.year == today.year:
				today_group.append(i)

		for i in individual_shares:
			if i.date_payment.month == today.month and i.date_payment.year == today.year:
				today_individual.append(i)

		return(today_individual, today_group)
		

	def fetch_recorded_payments(self):
		current_entry=self.fetch_current_entry()
		group_payments=current_entry.group.all()
		individual_payments=current_entry.individual.all()
		return(individual_payments, group_payments)

	def collect_payments(self):
		current_entry=self.fetch_current_entry()
		
		months_payments=self.fetch_this_months_payments()
		recorded_payments=self.fetch_recorded_payments()

		#groups
		for i in months_payments[1]:
			if i not in recorded_payments[1]:
				current_entry.individual.add(i.pk)


		#individuals
		for i in months_payments[0]:
			if i not in recorded_payments[0]:
				current_entry.individual.add(i.pk)

	def calculate_totals(self):
		current_entry=self.fetch_current_entry()

		recorded_payments=self.fetch_recorded_payments()
		total=0
		for i in recorded_payments[0]:
			total +=i.Amount


		for i in recorded_payments[1]:
			total +=i.Amount

		current_entry.total=total
		current_entry.save()



	



from Reports.views import Amorization_accounting	

class LoansMonthlyTasks(object):
	"""docstring for LoansDailyTasks"""
	def __init__(self):
		super(LoansMonthlyTasks, self).__init__()
		self.today=datetime.today()
	def loan_task(self):
		return Amorization_accounting(self.today.day, self.today.month, self.today.year)

	def get_loan_current_entry(self):
		entries=Loans_monthly_accounting_model.objects.all().order_by("-start") 
		try:
			return entries[0]

		except IndexError:

			new_entry=Loans_monthly_accounting_model()
			new_entry.save()

			return new_entry

	def recorded_payments(self):
		current_entry=self.get_loan_current_entry()
		individual=current_entry.individual_payments.all()
		group=current_entry.group_payments.all()
		return (individual, group)

	def fetch_months_payments(self):
		
		current_entry=self.get_loan_current_entry()
		lta=self.loan_task()
		interest=0
		outstanding=0
		individual_payments=lta.calculate_individual_loan_metrics('Monthly')
		group_payments=lta.calculate_group_loan_metrics('Monthly')
		recorded_payments=self.recorded_payments()
		#print(group_payments)
		#print(individual_payments)
		for i in group_payments[2]:
			if i not in recorded_payments[1]:
				current_entry.group_payments.add(i)

		for i in individual_payments[2]:
			if i not in recorded_payments[0]:
				current_entry.individual_payments.add(i)

		
		#print(group_payments[0], group_payments[2])
		#print(individual_payments[0])
		interest+=group_payments[0] 
		interest+=individual_payments[0] 


		outstanding += group_payments[1]
		outstanding += individual_payments[1]

		current_entry.interest_on_loans_total = interest
		current_entry.loans_outsanding_total = outstanding

		current_entry.save()





@background(schedule=1)

def schedule_all_daily_tasks():
	#####Loan Tasks
	lt=LoansMonthlyTasks()
	lt.fetch_months_payments()



	##### Simply picks up all shares payments of the current month both group and individuals and stores then inthe current_entry

	sh=SharesDailyTasks()
	sh.collect_payments()
	sh.calculate_totals()


	#picks up all DEBT payments in the current month that are not yet accounted for and calculates the totals
	##
	## 
	##
	#########  This are daily tasks preferably run at the end of day's operations


	dt=DebtsDailyTasks()

	dt.collect_fines_payments()
	
	dt.collect_charges_payments()
	dt.calculate_totals()

schedule_all_daily_tasks()
#mt.Add_new_entrys()
#print(mt.fetch_all_current_entries())

	#Add_new_entry(schedule=1)


def checks_to_perform_monthly(schedule=1):
	tasks_monthly=MonthlyTasks() #an instance of our monthly tasks

	#we first check that its the last day of the month 
	if tasks_monthly.check_if_month_is_done():


		#if True then we can perform the standard monthly accounting procedure

		#1 create new entry for use in the next month.., actually by midnight.

		tasks_monthly.Add_new_entrys()


		#2 record the date of the end month in the entry


		tasks_monthly.record_enddate()




checks_to_perform_monthly()

