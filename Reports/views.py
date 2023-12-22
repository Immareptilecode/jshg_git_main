
from Finance.models import IndividualDisbursed_Loan, GroupDisbursed_Loan, loan_repayment_register_individual, loan_repayment_register_group
from Finance.models import fines_payment_register_individual, charges_payment_register_individual, fines_payment_register_group, charges_payment_register_group, Share, gshare
from .models import Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income, Shares_Noncontribution_monthly_income, LoanInterest_fines_monthly_income, SharesContribution_monthly_income, Loans_monthly_accounting_model, LateReceipt_monthly_income


import calendar
from django.shortcuts import render
from datetime import datetime
from datetime import date
from datetime import timedelta


all_monthly_models=[SharesContribution_monthly_income, Loans_monthly_accounting_model, LoanInterest_fines_monthly_income, Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income, Shares_Noncontribution_monthly_income]
daily_model_guide={"charges":[Loanform_monthly_income, Exitfee_monthly_income, New_membership_monthly_income, Office_monthly_income], 'fines':[LoanInterest_fines_monthly_income, Loanfines_monthly_income, Absence_monthly_income, Cashfines_monthly_income, Shares_Noncontribution_monthly_income, LateReceipt_monthly_income]}

class Amorization_accounting(object):
	"""docstring for Amorization_accounting"""
	def __init__(self, day, month, year):
		super(Amorization_accounting, self).__init__()
		self.given_date=date(year, month, day)

	def get_all_individual_loans(self):
		loans=IndividualDisbursed_Loan.objects.all()

		return loans
	def get_all_group_loans(self):
		loans=GroupDisbursed_Loan.objects.all()

		return loans
	def month_has_payments(self):
		month_days=calendar.monthrange(self.given_date.year, self.given_date.month)[1]
		individuals=loan_repayment_register_individual.objects.filter(date_payment__lte=self.given_date +timedelta(days=month_days), date_payment__gte=self.given_date)
		groups=loan_repayment_register_group.objects.filter(date_payment__lte=self.given_date +timedelta(days=month_days), date_payment__gte=self.given_date)
		if len(individuals) == 0 and len(groups) == 0:
			return False
		else:
			return True
	


	def get_payments_individual(self, loan):
		payments=loan_repayment_register_individual.objects.filter(loan=loan)#.exclude(date)
		return payments

	def get_payments_group(self, loan):
		payments=loan_repayment_register_group.objects.filter(loan=loan)
		return payments

	def fetch_amorization_chart(self, loan):
		payments=self.get_payments_individual(loan)
		ints=0.01
		loan_amor_list=[]
		insta_start=1
		loaned_amount=loan.Amount
		for i in payments:
			monthly_dict={}


			if insta_start == 1:
				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount
				


				#easy...
				monthly_dict['loan_balance']=loaned_amount - (i.Amount -(loaned_amount * ints))
				monthly_dict['interest_charged']=loaned_amount * ints
				monthly_dict['payment_id']=i.pk
				
				#print( 'first')
			else:
				last_payment=loan_amor_list[len(loan_amor_list)-1]
				#print (last_payment, 'i')
				interest_charged_last=float(last_payment['loan_balance']) * ints
				#print(interest_charged_last, 'i')
				loan_bal_last=last_payment['loan_balance'] 

				amount_deductable=i.Amount -interest_charged_last # the difference between payment made and last intrerest charged 
				current_loan_bal = float(loan_bal_last)-amount_deductable
				current_intrest=current_loan_bal * 0.01
				
				#print(last_payment['interest_charged'])


				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount

				#easy...

				monthly_dict['loan_balance']=format(current_loan_bal, '.2f')
				
				monthly_dict['interest_charged']=format(interest_charged_last, '.2f') 
				monthly_dict['payment_id']=i.pk
				#if current_loan_bal == 0 or current_loan_bal < 2:
					#theloan=GroupDisbursed_Loan.objects.get(id=loan.id)
					#theloan.re_paid=True
					#theloan.save()
				
			insta_start += 1
			loan_amor_list.append(monthly_dict)



		#for i in loan_amor_list:
			#print (i)	
		#print(loan_amor_list)
			#print(self.payments.index(i))


		#print(len(self.payments))


		return loan_amor_list

	def fetch_amorization_chart_group(self, loan):
		payments=self.get_payments_group(loan)
		ints=0.01
		loan_amor_list=[]
		insta_start=1
		loaned_amount=loan.Amount
		for i in payments:
			monthly_dict={}


			if insta_start == 1:
				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount
				


				#easy...
				monthly_dict['loan_balance']=loaned_amount - (i.Amount -(loaned_amount * ints))
				monthly_dict['interest_charged']=loaned_amount * ints
				monthly_dict['payment_id']=i.pk

				#print( 'first')
			else:
				last_payment=loan_amor_list[len(loan_amor_list)-1]
				#print (last_payment, 'i')
				interest_charged_last=float(last_payment['loan_balance']) * ints
				#print(interest_charged_last, 'i')
				loan_bal_last=last_payment['loan_balance'] 

				amount_deductable=i.Amount -interest_charged_last # the difference between payment made and last intrerest charged 
				current_loan_bal = float(loan_bal_last)-amount_deductable
				current_intrest=current_loan_bal * 0.01
				
				#print(last_payment['interest_charged'])


				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount

				#easy...

				monthly_dict['loan_balance']=format(current_loan_bal, '.2f')
				
				monthly_dict['interest_charged']=format(interest_charged_last, '.2f') 
				monthly_dict['payment_id']=i.pk

				#if current_loan_bal == 0 or current_loan_bal < 2:
					#theloan=GroupDisbursed_Loan.objects.get(id=loan.id)
					#theloan.re_paid=True
					#theloan.save()
				
			insta_start += 1
			loan_amor_list.append(monthly_dict)



		#for i in loan_amor_list:
			#print (i)	
		#print(loan_amor_list)
			#print(self.payments.index(i))


		#print(len(self.payments))


		return loan_amor_list	

	def calculate_individual_loan_metrics(self, mode):
		interest_earned=0
		outstanding_loan_totals=0
		evidence_payments=[]
		all_loans=self.get_all_individual_loans()
		repaid_loans=[]
		outstanding_loans=[]

		for i in all_loans:
			if i.re_paid == True :
				repaid_loans.append(i)

		for i in all_loans:
			if i.re_paid == False:
				outstanding_loans.append(i)

		if mode == 'Annual':



			for i in repaid_loans:
				chart=self.fetch_amorization_chart(i)
				for x in chart:
					if x['date'].year == self.given_date.year:

					
						interest_earned += float(x['interest_charged'])

			for i in outstanding_loans:
				chart=self.fetch_amorization_chart(i)
				for x in chart:
					if x['date'].year == self.given_date.year:

					
						interest_earned += float(x['interest_charged'])

					
				try:	
					outstanding_loan_totals += float(chart[len(chart)-1]['loan_balance'])
				except IndexError:
					if len(chart)==0:
						print('new loan')
						outstanding_loan_totals += i.Amount
					else:

						print('done adding outstanding loans')
					
			#print(interest_earned , 'intrerest earned on loans')
			#print(outstanding_loan_totals , 'outstanding loans')
			return(interest_earned, outstanding_loan_totals, evidence_payments)
		elif mode == 'Monthly':
			for i in repaid_loans:
				chart=self.fetch_amorization_chart(i)
				for x in chart:
					if x['date'].month == self.given_date.month and x['date'].year == self.given_date.year:
						interest_earned += float(x['interest_charged'])
						evidence_payments.append(x['payment_id'])

			for i in outstanding_loans:
				chart=self.fetch_amorization_chart(i)
				
				for x in chart:
					if x['date'].month == self.given_date.month and x['date'].year == self.given_date.year:
						interest_earned += float(x['interest_charged'])
						evidence_payments.append(x['payment_id'])
					
				try:
					outstanding_loan_totals += float(chart[len(chart)-1]['loan_balance'])
				except IndexError:
					if len(chart)==0:
						print('new loan')
						outstanding_loan_totals += i.Amount
					else:

						print('done adding outstanding loans')

			#print(interest_earned , 'intrerest earned on loans')
			#print(outstanding_loan_totals , 'outstanding loans')

		return(interest_earned, outstanding_loan_totals, evidence_payments)



	def calculate_group_loan_metrics(self, mode):
		interest_earned=0
		outstanding_loan_totals=0
		all_loans=self.get_all_group_loans()
		repaid_loans=[]
		outstanding_loans=[]
		evidence_payments=[]

		for i in all_loans:
			if i.re_paid == True :
				repaid_loans.append(i)

		for i in all_loans:
			if i.re_paid == False:
				outstanding_loans.append(i)


		if mode == 'Annual':

			for i in repaid_loans:
				chart=self.fetch_amorization_chart_group(i)
				for x in chart:
					if x['date'].year == self.given_date.year:

					
						interest_earned += float(x['interest_charged'])
					
			for i in outstanding_loans:
				chart=self.fetch_amorization_chart_group(i)
				for x in chart:
					if x['date'].year == self.given_date.year:

					
						interest_earned += float(x['interest_charged'])
				try:	
					outstanding_loan_totals += float(chart[len(chart)-1]['loan_balance'])
				except IndexError:
					if len(chart)==0:
						print('new loan')
						outstanding_loan_totals += i.Amount
					else:
				
						print('done adding outstanding loans')

					

			#print(interest_earned , 'intrerest earned on loans')
			#print(outstanding_loan_totals , 'outstanding loans')

			return(interest_earned, outstanding_loan_totals, evidence_payments)
		elif mode == 'Monthly':

			for i in repaid_loans:
				chart=self.fetch_amorization_chart_group(i)
				for x in chart:
					#print(x)
					if x['date'].month == self.given_date.month and x['date'].year == self.given_date.year:
						interest_earned += float(x['interest_charged'])
						evidence_payments.append(x['payment_id'])
			for i in outstanding_loans:
				chart=self.fetch_amorization_chart_group(i)
				for x in chart:
					if x['date'].month == self.given_date.month and x['date'].year == self.given_date.year:
						interest_earned += float(x['interest_charged'])
						evidence_payments.append(x['payment_id'])
					
				try:	
					outstanding_loan_totals += float(chart[len(chart)-1]['loan_balance'])

				except IndexError:
					if len(chart)==0:
						print('new loan')
						outstanding_loan_totals += i.Amount
					else:

						print('done adding outstanding loans')

			#print(interest_earned , 'intrerest earned from loans on the Month of %s, year %s.'% (today.strftime("%B"), year))
			#print(outstanding_loan_totals , 'outstanding loans')

			return(interest_earned, outstanding_loan_totals, evidence_payments)




class Shares_accounting_model_operations(object):
	"""docstring for Shares_accounting_model_operations"""
	def __init__(self, date):
		super(Shares_accounting_model_operations, self).__init__()
		self.given_date = date

	def create_new(self):
		newentry=SharesContribution_monthly_income(start=self.given_date)
		newentry.save()
		return newentry

	def get_entry(self):
		try:
  			entry=SharesContribution_monthly_income.objects.get(start=self.given_date)

		except SharesContribution_monthly_income.DoesNotExist:
  			return None
  		
		return entry

	def fetch_accounted_payments(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		return (individuals, groups )

	def fetch_all_payments(self, mode):

  		#payments specific to the accounting model for the month in the given date
		payments_individual=[] #any new payments made today
		payments_group=[]
		
		the_date=self.given_date
		individual=Share.objects.all()
		groups=gshare.objects.all()
		if mode == 'Annual':
			annual_total=0
			for i in individual:
				if  i.date_payment.year == the_date.year:
					payments_individual.append(i)
					annual_total += i.Amount

			for i in groups:
				if  i.date_payment.year == the_date.year:
					payments_group.append(i)
					annual_total += i.Amount

			return(annual_total, payments_individual, payments_group)


		elif mode == 'Monthly':

			monthly_total=0
			for i in individual:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_individual.append(i)
					monthly_total +=i.Amount

			for i in groups:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_group.append(i)
					monthly_total +=i.Amount

			return(monthly_total, payments_individual, payments_group)
		

	def collect_shares_payments(self, entry, allpayments):

		recorded_payments=self.fetch_accounted_payments(entry)
		unaccounted_for=allpayments
		#groups
		for i in unaccounted_for[2]:
			if i not in recorded_payments[1]:
				entry.group.add(i)
		for i in unaccounted_for[1]:
			if i not in recorded_payments[0]:
				entry.individual.add(i)

	def calculate_totals(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		total=0

		for i in individuals:
			total += i.Amount

		for i in groups:
			total += i.Amount

		entry.total=total
		entry.save()


class charges_accounting_model_operations(object):

	def __init__(self, date, model):
		super(charges_accounting_model_operations, self).__init__()
		self.given_date = date
		self.model=model
		self.the_given_months_entry=self.get_entry()
		
	def create_new(self):

		newentry=self.model(start=self.given_date)
		newentry.save()

		return newentry

	def get_entry(self):
		try:
  			entry=self.model.objects.get(start=self.given_date)

		except self.model.DoesNotExist:
  			return None
  		
		return entry
	def fetch_accounted_payments(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		return (individuals, groups )



	def fetch_all_payments(self, mode, entry):

  		#payments specific to the accounting model for the month in the given date
  		
		random_accounting_model_entry=entry

		try:
  			model_name=random_accounting_model_entry.model_name()

		except AttributeError:
		
			return {'error': 'NO ENTRY FOR THIS MONTH'}
		

		payments_individual=[] #any new payments made today
		payments_group=[]	
		#any new payments made today
		the_date=self.given_date
		individual=charges_payment_register_individual.objects.all().filter(charge__Particulars__in = model_name)
		groups=charges_payment_register_group.objects.all().filter(charge__Particulars__in =model_name )
		if mode == 'Annual':
			annual_total=0
			for i in individual:
				if  i.date_payment.year == the_date.year:
					payments_individual.append(i)
					annual_total += i.Amount

			for i in groups:
				if  i.date_payment.year == the_date.year:
					payments_group.append(i)
					annual_total += i.Amount

			return(annual_total, payments_individual, payments_group)


		elif mode == 'Monthly':

			monthly_total=0
			for i in individual:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_individual.append(i)
					monthly_total +=i.Amount

			for i in groups:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_group.append(i)
					monthly_total +=i.Amount

			return(monthly_total, payments_individual, payments_group)


	def collect_charges_payments(self, entry, allpayments):
		recorded_payments=self.fetch_accounted_payments(entry)
		unaccounted_for=allpayments
		#groups
		for i in unaccounted_for[2]:
			if i not in recorded_payments[1]:
				entry.group.add(i)
		for i in unaccounted_for[1]:
			if i not in recorded_payments[0]:
				entry.individual.add(i)

	def calculate_totals(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		total=0

		for i in individuals:
			total += i.Amount

		for i in groups:
			total += i.Amount

		entry.total=total
		entry.save()

class fines_accounting_model_operations(object):

	def __init__(self, date, model):
		super(fines_accounting_model_operations, self).__init__()
		self.given_date = date
		self.model=model
		self.the_given_months_entry=self.get_entry()
		
	def create_new(self):

		newentry=self.model(start=self.given_date)
		newentry.save()

		return newentry

	def get_entry(self):
		try:
  			entry=self.model.objects.get(start=self.given_date)

		except self.model.DoesNotExist:
  			return None
  		
		return entry
	def fetch_accounted_payments(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		return (individuals, groups )



	def fetch_all_payments(self, mode, entry):

  		#payments specific to the accounting model for the month in the given date
  		
		random_accounting_model_entry=entry

		try:
  			model_name=random_accounting_model_entry.model_name()

		except AttributeError:
		
			return {'error': 'NO ENTRY FOR THIS MONTH'}
		
		payments_individual=[] #any new payments made today
		payments_group=[]	
		#any new payments made today
		the_date=self.given_date
		individual=fines_payment_register_individual.objects.all().filter(fine__Particulars__in = model_name)
		groups=fines_payment_register_group.objects.all().filter(fine__Particulars__in =model_name )
		if mode == 'Annual':
			annual_total=0
			for i in individual:
				if  i.date_payment.year == the_date.year:
					payments_individual.append(i)
					annual_total += i.Amount

			for i in groups:
				if  i.date_payment.year == the_date.year:
					payments_group.append(i)
					annual_total += i.Amount

			return(annual_total, payments_individual, payments_group)


		elif mode == 'Monthly':

			monthly_total=0
			for i in individual:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_individual.append(i)
					monthly_total +=i.Amount

			for i in groups:
				if i.date_payment.month == the_date.month and i.date_payment.year == the_date.year:
					payments_group.append(i)
					monthly_total +=i.Amount

			return(monthly_total, payments_individual, payments_group)


	def collect_fines_payments(self, entry, allpayments):
		recorded_payments=self.fetch_accounted_payments(entry)
		unaccounted_for=allpayments
		#groups
		for i in unaccounted_for[2]:
			if i not in recorded_payments[1]:
				entry.group.add(i)
		for i in unaccounted_for[1]:
			if i not in recorded_payments[0]:
				entry.individual.add(i)

	def calculate_totals(self, entry):
		individuals=entry.individual.all()
		groups=entry.group.all()
		total=0

		for i in individuals:
			total += i.Amount

		for i in groups:
			total += i.Amount

		entry.total=total
		entry.save()


class Debts_accounting_logic(object):

	def __init__(self, date):
		super(Debts_accounting_logic, self).__init__()
		self.requested_date=date
		self.payment_data_is_available=self.check_payment_data_availability()
	

	def check_payment_data_availability(self):
		month_days=calendar.monthrange(self.requested_date.year, self.requested_date.month)[1]
		fines_i=fines_payment_register_individual.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)
		fines_g=fines_payment_register_group.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)

		charges_i=charges_payment_register_individual.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)
		
		charges_g=charges_payment_register_group.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)

		if len(fines_i) != 0 or len(fines_g) != 0 or len(charges_i) != 0  or len(charges_g) != 0  :
			
			
			return True

		else:
			# if nothing exists 
			return False

	def fetch_all_charges_reports(self):
		full_dict={}
		#annual_dict={}
		for model in daily_model_guide['charges']:
			model_clerk=charges_accounting_model_operations(self.requested_date, model)
			
			try:
				entry=model_clerk.get_entry()
				charges_annual_total=model_clerk.fetch_all_payments('Annual', entry)[0]
				charges_monthly_total=model_clerk.fetch_all_payments('Monthly', entry)[0]

				# when all goes well
			

				full_dict[entry.model_name()[0]]=[charges_monthly_total, charges_annual_total]
					
				#print(model, charges_monthly_total, charges_annual_total)
			except KeyError:
				#for some reason the data may miss the entry of a model so we make two checks
				#This is the first
				#print('no data for model: %s' % model, model_clerk.get_entry())
				try:

				
				#This is the second
					the_entry_missed=model_clerk.get_entry()
					# we find the entry manually

					#if the_entry blah blah blah returns None 

					#then the following two statements will have a key error due to the indexing

					#the fetch all payments function returns a dictionary for an error and a list of resulsts when successful.
					charges_annual_total=model_clerk.fetch_all_payments('Annual', the_entry_missed)[0]
					charges_monthly_total=model_clerk.fetch_all_payments('Monthly', the_entry_missed)[0]

					full_dict[entry.model_name()[0]]=[charges_monthly_total, charges_annual_total]
				except KeyError:
					#print('not kidding %s ' % model)
					#so then we know its not kidding and we proceed to create a new entry eventually loading it up.
					if self.payment_data_is_available:
						newly_created=model_clerk.create_new()
						model_clerk.collect_charges_payments(newly_created, model_clerk.fetch_all_payments('Monthly', newly_created))
						model_clerk.calculate_totals(newly_created)
						
						#now compile the results
						# when something went wrong
						charges_annual_total=model_clerk.fetch_all_payments('Annual', newly_created)[0]
						charges_monthly_total=model_clerk.fetch_all_payments('Monthly', newly_created)[0]

						full_dict[newly_created.model_name()[0]]=[charges_monthly_total, charges_annual_total]

			#now compile the results			
				
					
		return full_dict


	def fetch_all_fines_reports(self):
		full_dict={}
	
		for model in daily_model_guide['fines']:
			model_clerk=fines_accounting_model_operations(self.requested_date, model)
			
			try:
				entry=model_clerk.get_entry()
				fines_annual_total=model_clerk.fetch_all_payments('Annual', entry)[0]
				fines_monthly_total=model_clerk.fetch_all_payments('Monthly', entry)[0]

				# when all goes well
			

				full_dict[entry.model_name()[0]]=[fines_monthly_total, fines_annual_total]
					
				#print(model, charges_monthly_total, charges_annual_total)
			except KeyError:
				#for some reason the data may miss the entry of a model so we make two checks
				#This is the first
				#print('no data for model: %s' % model, model_clerk.get_entry())
				try:

				
				#This is the second
					the_entry_missed=model_clerk.get_entry()
					# we find the entry manually

					#if the_entry blah blah blah returns None 

					#then the following two statements will have a key error due to the indexing

					#the fetch all payments function returns a dictionary for an error and a list of resulsts when successful.
					fines_annual_total=model_clerk.fetch_all_payments('Annual', the_entry_missed)[0]
					fines_monthly_total=model_clerk.fetch_all_payments('Monthly', the_entry_missed)[0]

					full_dict[entry.model_name()[0]]=[fines_monthly_total, fines_annual_total]
				except KeyError:
					#print('not kidding %s ' % model)
					#so then we know its not kidding and we proceed to create a new entry eventually loading it up.
					if self.payment_data_is_available:
						newly_created=model_clerk.create_new()
						model_clerk.collect_fines_payments(newly_created, model_clerk.fetch_all_payments('Monthly', newly_created))
						model_clerk.calculate_totals(newly_created)
						
						#now compile the results
						# when something went wrong
						fines_annual_total=model_clerk.fetch_all_payments('Annual', newly_created)[0]
						fines_monthly_total=model_clerk.fetch_all_payments('Monthly', newly_created)[0]

						full_dict[newly_created.model_name()[0]]=[fines_monthly_total, fines_annual_total]

			#now compile the results			
				
					
		return full_dict

					#newly_created=model_clerk.create_new()
					#print(newly_created.start)
		

class shares_accounting_logic(object):

	def __init__(self, date):
		super(shares_accounting_logic, self).__init__()
		self.requested_date=date
		self.payment_data_is_available=self.check_payment_data_availability()
	

	def check_payment_data_availability(self):
		month_days=calendar.monthrange(self.requested_date.year, self.requested_date.month)[1]
		shares_i=Share.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)
		shares_g=gshare.objects.filter(date_payment__lte=self.requested_date +timedelta(days=month_days), date_payment__gte=self.requested_date)

		
		if len(shares_i) != 0 or len(shares_g) != 0:
			
			
			return True

		else:
			# if nothing exists 
			return False

	def fetch_all_shares_reports(self):
		full_dict={}
		#annual_dict={}
		
		model_clerk=Shares_accounting_model_operations(self.requested_date)
			
		try:
			entry=model_clerk.get_entry()
		
				# when all goes well
			shares_annual_total=model_clerk.fetch_all_payments('Annual')[0]
			shares_monthly_total=model_clerk.fetch_all_payments('Monthly')[0]

			full_dict['shares']=[shares_monthly_total, shares_annual_total]
					
				#print(model, charges_monthly_total, charges_annual_total)
		except KeyError:
				#for some reason the data may miss the entry of a model so we make two checks
				#This is the first
				#print('no data for model: %s' % model, model_clerk.get_entry())
			try:

				
				#This is the second
				the_entry_missed=model_clerk.get_entry()
				# we find the entry manually

				#if the_entry blah blah blah returns None 

				#then the following two statements will have a key error due to the indexing

				#the fetch all payments function returns a dictionary for an error and a list of resulsts when successful.
				shares_annual_total=model_clerk.fetch_all_payments('Annual')[0]
				shares_monthly_total=model_clerk.fetch_all_payments('Monthly')[0]

				full_dict['shares']=[shares_monthly_total, shares_annual_total]
			except KeyError:
				#print('not kidding %s ' % model)
				#so then we know its not kidding and we proceed to create a new entry eventually loading it up.
				if self.payment_data_is_available:
					newly_created=model_clerk.create_new()
					model_clerk.collect_shares_payments(newly_created, model_clerk.fetch_all_payments('Monthly'))
					model_clerk.calculate_totals(newly_created)
						
						#now compile the results
						# when something went wrong
					shares_annual_total=model_clerk.fetch_all_payments('Annual')[0]
					shares_monthly_total=model_clerk.fetch_all_payments('Monthly')[0]
					full_dict['shares']=[shares_monthly_total, shares_annual_total]

			#now compile the results			
				
					
		return full_dict

#Django views

from django.views import View
from django.http import HttpResponse
import json
from .forms import date_form
class Reports_home(View):
	form_class=date_form
	def get(self, request, **kwargs):
		
		


		return render(request, 'reports_summary.html', {'form':date_form})


	def post(self, request, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			#creating a date object
			da=form['date'].value()
			splited_date=da.split("-")
			day=int(splited_date[2])
			month=int(splited_date[1])
			year=int(splited_date[0])
			date_requested=date(year, month, day)


			if day != 1:
				return render(request, 'reports_summary.html', {'form':date_form})
			else:

				#DEBTS
				gh=Debts_accounting_logic(date_requested)
				charges=gh.fetch_all_charges_reports()
				fines=gh.fetch_all_fines_reports()

				# shares

				sh=shares_accounting_logic(date_requested)
				shares=sh.fetch_all_shares_reports()
				#LOANS

				lf=Amorization_accounting(day, month, year)
				interest_earned_monthly=0
				interest_earned_annual=0
				outstanding_loans=0
				if lf.month_has_payments():
					individual_monthly=lf.calculate_individual_loan_metrics('Monthly')
					group_monthly=lf.calculate_group_loan_metrics('Monthly')

					individual_annual=lf.calculate_individual_loan_metrics('Annual')
					group_annual=lf.calculate_group_loan_metrics('Annual')


					year_individual=interest_earned_monthly
					interest_earned_monthly += individual_monthly[0] #interest
					interest_earned_monthly += group_monthly[0] #interest

					outstanding_loans += group_monthly[1]   #outstanding loans total
					outstanding_loans += individual_monthly[1]   #outstanding loans total

					interest_earned_annual += individual_annual[0]
					interest_earned_annual += group_annual[0]

				#print(date_requested.year)

				return render(request, 'reports_summary.html', {'form':date_form, 'charges':charges, 'fines':fines, 'date_viewing':date_requested, 'month_viewing':date_requested.strftime("%B"), 'loan_interest_month':round(interest_earned_monthly, 2), 'loan_interest_year':round(interest_earned_annual, 2), 'loans_outstanding':outstanding_loans, 'shares':shares})
class charges_reports(View):

	
	def get(self, request, **kwargs):

		df=date(self.kwargs['year'], self.kwargs['month'],  self.kwargs['day'])
		gh=Debts_accounting_logic(df)
		charges_report=gh.fetch_all_charges_reports()
		if len(charges_report[0]) ==0 and len(charges_report[1]) ==0:
			return HttpResponse(json.dumps([]), content_type="application/json")
		else:

			return HttpResponse(json.dumps([charges_report[1], charges_report[0]]), content_type="application/json")



class fines_reports(View):
	
	def get(self, request, **kwargs):

		df=date(self.kwargs['year'], self.kwargs['month'],  self.kwargs['day'])
		gh=Debts_accounting_logic(df)
		fines_report=gh.fetch_all_fines_reports()
		if len(fines_report[0]) ==0 and len(fines_report[1]) ==0:
			return HttpResponse(json.dumps([]), content_type="application/json")
		else:

			return HttpResponse(json.dumps([fines_report[1], fines_report[0]]), content_type="application/json")

class loan_reports(View):
	
	def get(self, request, **kwargs):
		interest_earned_monthly=0
		outstanding_loans=0

		interest_earned_annual=0
		lf=Amorization_accounting(self.kwargs['day'], self.kwargs['month'], self.kwargs['year'])
		if lf.month_has_payments():
			individual_monthly=lf.calculate_individual_loan_metrics('Monthly')
			group_monthly=lf.calculate_group_loan_metrics('Monthly')

			individual_annual=lf.calculate_individual_loan_metrics('Annual')
			group_annual=lf.calculate_group_loan_metrics('Annual')


			year_individual=interest_earned_monthly
			interest_earned_monthly += individual_monthly[0] #interest
			interest_earned_monthly += group_monthly[0] #interest

			outstanding_loans += group_monthly[1]   #outstanding loans total
			outstanding_loans += individual_monthly[1]   #outstanding loans total

			interest_earned_annual += individual_annual[0]
			interest_earned_annual += group_annual[0]



			return HttpResponse(json.dumps([interest_earned_annual, interest_earned_monthly, outstanding_loans]), content_type="application/json")
		else:
			return HttpResponse(json.dumps([]), content_type="application/json")
