from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views import View
from Membership.models import Member, Groups
from .models import Share, gshare, IndividualDisbursed_Loan, loan_repayment_register_individual, GroupDisbursed_Loan, loan_repayment_register_individual, loan_repayment_register_group, loan_repayment_register_individual
import json
from django.http import HttpResponse
from rest_framework import generics
from django.http import Http404
from io import BytesIO
from .serializers import ShareSerializer, GroupShareSerializer, individual_loanSerializer, group_loanSerializer, individual_registerSerializer, group_registerSerializer, ShareCapitalSerializer, GroupShareCapitalSerializer
from django.views.generic import ListView
from django.utils import timezone	
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from .forms import individual_loan_form, group_loan_form, individual_charges_payment_form, individual_fines_payment_form, individual_charges_record_form, individual_loan_offset, group_loan_offset


from Reports.models import Share_Capital_deductions_individual, Share_Capital_deductions_group, Loanoffset_deductions_individual, Loanoffset_deductions_group



# SHARES RELATED OPS

class Shares_Tasks_base():
	def __init__(self, identity, task_specification):
	
		self.user_id=identity.pk
		self.user_type=self.fetch_specs(task_specification)

	def fetch_specs(self, categ):
		if categ == 'g':
			return "GROUP"
		elif categ == 'i':
			return "INDIVIDUAL"
		else:
			raise TypeError("unrecognized_entry")

	def calculate_net_shares(self):
		gross_shares=0
		netshares=0
		deductions=0
		# initializing the data we need t
		if self.user_type == "GROUP":
			try:
				user=Groups.objects.get(id=self.user_id)
			except Groups.DoesNotExist:
				return 'Dont play me! There is no such group buddy.'

	
		
			share_payments=gshare.objects.filter(group=user) 
		
			
			#load up the gross shares total
			for i in share_payments:
				gross_shares +=i.Amount

			#deductions
			sharecap=Share_Capital_deductions_group.objects.filter(group=user)
			loan_offset=Loanoffset_deductions_group.objects.filter(loan__Borrower=user)
			for i in sharecap:
				deductions += i.Amount

			for i in loan_offset:
				deductions +=i.balance_amount
			

		elif self.user_type == "INDIVIDUAL":
			try:
				user=Member.objects.get(id=self.user_id)
			except Member.DoesNotExist:
				return 'Dont play me! There is no such individual buddy.'
			
			share_payments=Share.objects.filter(member=user)

			#load up the gross shares total
			for i in share_payments:
				gross_shares +=i.Amount

			#deductions
			sharecap=Share_Capital_deductions_individual.objects.filter(individual=user)
			loan_offset=Loanoffset_deductions_individual.objects.filter(loan__Borrower=user)

			for i in sharecap:
				deductions += i.Amount

			for i in loan_offset:
				deductions +=i.balance_amount

		# final math
		netshares = gross_shares - deductions

		return netshares


class calculate_shares(View):
	# does the math for shares less deductions
	def get(self, request, **kwargs):
		the_person=Member.objects.get(id=self.kwargs['mid'])
		sh_ops=Shares_Tasks_base(the_person, 'i')
		
		netshares =sh_ops.calculate_net_shares()
		shares_list=[]
		shares_list.append(str(netshares))


		return HttpResponse(json.dumps(shares_list), content_type="application/json")


class calculate_shares_group(View):
	# does the math for shares less deductions
	def get(self, request, **kwargs):
		the_group=Groups.objects.get(id=self.kwargs['mid'])
		sh_ops=Shares_Tasks_base(the_group, 'g')

		netshares = sh_ops.calculate_net_shares()
		shares_list=[]
		shares_list.append(str(netshares))


		return HttpResponse(json.dumps(shares_list), content_type="application/json")

class shareslist(generics.ListCreateAPIView):
	serializer_class=ShareSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Member.objects.get(id=self.kwargs['mid'])
		queryset=Share.objects.filter(member=cstmr).order_by('-date_payment')
		return queryset
	

class Groupshareslist(generics.ListCreateAPIView):
	serializer_class=GroupShareSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Groups.objects.get(id=self.kwargs['mid'])
		queryset=gshare.objects.filter(group=cstmr)
		return queryset




# SHARE CAPITAL REALATED OPS
class calculate_sharecapital(View):
	# does the math for shares less deductions
	def get(self, request, **kwargs):
		result=[]
		the_person=Member.objects.get(id=self.kwargs['mid'])
		deductions=Share_Capital_deductions_individual.objects.filter(individual=the_person)
		total_deductions=0
		#share capital deductions

	

		for c in deductions:
			
			total_deductions +=c.Amount

		message_objectdict={}
			
		message_objectdict['total']= str(total_deductions)
			
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
		result.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(result), content_type="application/json")

class calculate_sharecapitalGroup(View):
	# does the math for shares less deductions
	def get(self, request, **kwargs):
		result=[]
		the_group=Groups.objects.get(id=self.kwargs['mid'])
		deductions=Share_Capital_deductions_group.objects.filter(group=the_group)
		total_deductions=0
		#share capital deductions

	

		for c in deductions:
			
			total_deductions +=c.Amount

		message_objectdict={}
			
		message_objectdict['total']= str(total_deductions)
			
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
		result.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(result), content_type="application/json")

class shareCapital_individual(generics.ListCreateAPIView):
	serializer_class=ShareCapitalSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Member.objects.get(id=self.kwargs['mid'])
		queryset=Share_Capital_deductions_individual.objects.filter(individual=cstmr).order_by('-date')
		return queryset

class shareCapital_group(generics.ListCreateAPIView):
	serializer_class=GroupShareCapitalSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Member.objects.get(id=self.kwargs['mid'])
		queryset=Share.objects.filter(group=cstmr).order_by('-date')
		return queryset






#LOAN REALATED OPS

class Loan_tasks_base():
	def __init__(self, mid, md):
		self.mode=md
		self.user_id=mid
		self.customer=self.get_customer()
		self.current_loan= self.get_current_loan()
		
		

	def get_customer(self):
		if self.mode =='i':
			m=Member.objects.get(id=self.user_id)
			return m
		elif self.mode == 'g':
			g=Groups.objects.get(id=self.user_id)
			return g

	def get_current_loan(self):
		if self.mode == 'g':
			c_loan=GroupDisbursed_Loan.objects.filter(Borrower=self.customer).filter(re_paid=False)
			theloan=GroupDisbursed_Loan.objects.get(id=c_loan[0].id)
			return theloan
		elif self.mode == 'i':
			c_loan=IndividualDisbursed_Loan.objects.filter(Borrower=self.customer).filter(re_paid=False)
			theloan=IndividualDisbursed_Loan.objects.get(id=c_loan[0].id)
			return theloan

	def mark_as_repaid(self):
		loan=self.current_loan
		loan.re_paid=True
		loan.save()

class offsetloan_individual(View):
	form_class =individual_loan_offset
	def post(self, request, * args, ** kwargs):
		new_data=request.POST
	
		
		form = self.form_class(new_data)
		
		if form.is_valid():
			member=Member.objects.get(id=self.kwargs['mid'])
			offset_amount=float(request.POST['balance_amount'])
			remaining_loan_bal=float(self.kwargs['loan_balance'])
			sh=Shares_Tasks_base(member, 'i')
			shares=sh.calculate_net_shares()
			if offset_amount < shares and remaining_loan_bal == offset_amount:
				lt=Loan_tasks_base(self.kwargs['mid'], 'i')
				lt.mark_as_repaid()
				form.save()
				return HttpResponse('success')

			elif remaining_loan_bal != offset_amount:
				
				return HttpResponse('FAILED Cause Amount Not Same')

			elif offset_amount > shares:
				return HttpResponse('FAILED Cause Shares Not Enough')

			
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json(), new_data['loan'])
			return HttpResponse(form.errors.as_json())



class offsetloan_group(View):
	form_class =group_loan_offset
	def post(self, request, * args, ** kwargs):
		new_data=request.POST
	
		
		form = self.form_class(new_data)
		
		if form.is_valid():
			group=Groups.objects.get(id=self.kwargs['mid'])
			offset_amount=float(request.POST['balance_amount'])
			remaining_loan_bal=float(self.kwargs['loan_balance'])
			sh=Shares_Tasks_base(group, 'g')
			shares=sh.calculate_net_shares()
			if offset_amount < shares and remaining_loan_bal == offset_amount:
				lt=Loan_tasks_base(self.kwargs['mid'], 'g')
				lt.mark_as_repaid()
				form.save()
				return HttpResponse('success')

			elif remaining_loan_bal != offset_amount:
				
				return HttpResponse('FAILED Cause Amount Not Same')

			elif offset_amount > shares:
				return HttpResponse('FAILED Cause Shares Not Enough')

			
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json(), new_data['loan'])
			return HttpResponse('FAILED')





class processLoan(View):
	form_class =individual_loan_form
	def post(self, request, * args, ** kwargs):
		new_data=request.POST
		GS=request.POST['gurantor'].split(',')
		
		form = self.form_class(new_data)
		
		if form.is_valid():
			all_loans=IndividualDisbursed_Loan.objects.filter(Borrower=new_data['Borrower'])
			unsaved_form=form.save(commit=False)
			for i in all_loans:
				if i.re_paid == False:
					
					return HttpResponse('UNPAID_LOAN')
			for i in GS:
				unsaved_form.gurantor.add(i)
			unsaved_form.save()	
			#print(unsaved_form.gurantor, 'hakuna ama?')
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			#print(form.errors.as_json())
			return HttpResponse('FAILED')


class processLoan_group(View):
	form_class =group_loan_form
	def post(self, request, * args, ** kwargs):
		new_data=request.POST
		#print(new_data)
		GS=request.POST['gurantor'].split(',')
		#print(len(GS))
		form = self.form_class(new_data)
		if form.is_valid():
			all_loans=GroupDisbursed_Loan.objects.filter(Borrower=new_data['Borrower'])
			unsaved_form=form.save(commit=False)

			for i in all_loans:
				if i.re_paid == False:
					
					return HttpResponse('UNPAID_LOAN')
			for i in GS:
				unsaved_form.gurantor.add(i)
			unsaved_form.save()	
			
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			#print(form.errors.as_json()) how you can pass errors back to the frontend
			return HttpResponse('FAILED')

class individual_loan(generics.ListCreateAPIView):
	serializer_class=individual_loanSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Member.objects.get(membership_no=self.kwargs['mid'])
		queryset=IndividualDisbursed_Loan.objects.filter(member=cstmr)

		return queryset


from django.shortcuts import render

class Amorize_on_the_spot(object):
	
	def __init__(self, current_loan_id):
		self.current_loan_id = current_loan_id # queryset of all payments related to the specific loan
		self.loan=self.get_loan() # this should be replaced with the loan object being operated on
		self.chart_list=[]  #cant play around with the class variables alot as its hard to play around with custom objects in django so we are stuck to istance variables
		self.decided_amount=self.get_loan_monthly_payment()
		self.ints= 0.01
		self.payments=self.get_payments()
		

	def scan_payment(self):
		decided_amount=4442.44
		if self.payment < decided_amount:
			print('underpayment')

		elif self.payment > decided_amount:
			print('overpayment')

	def process_payments(self):
		return 5000

	def get_loan(self):
		l=IndividualDisbursed_Loan.objects.get(id=self.current_loan_id)
		return l


	def get_loan_monthly_payment(self):
		months=self.loan.installments
		principal=self.loan.Amount
		ints=0.01
		monthly=(ints*principal)/(1-(1+ints)**-months)   # formula for periodic payment
		return monthly



	def get_payments(self):
		l=IndividualDisbursed_Loan.objects.get(id=self.current_loan_id)
		payments= loan_repayment_register_individual.objects.filter(loan=l).order_by('date_payment')
		#print(payments)
		return payments

	#end of initialization sensitive methods
	
	def fetch_amorization_chart(self):
		loan_amor_list=[]
		insta_start=1
		loaned_amount=self.loan.Amount
		for i in self.payments:
			monthly_dict={}


			if insta_start == 1:
				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount
				


				#easy...
				monthly_dict['loan_balance']=loaned_amount - (i.Amount -(loaned_amount * self.ints))
				monthly_dict['interest_charged']=loaned_amount * self.ints
				
				#print( 'first')
			else:
				last_payment=loan_amor_list[len(loan_amor_list)-1]
				#print (last_payment, 'i')
				interest_charged_last=float(last_payment['loan_balance']) * self.ints
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

				if current_loan_bal == 0 or current_loan_bal < 2:
					theloan=IndividualDisbursed_Loan.objects.get(id=self.loan.id)
					theloan.re_paid=True
					theloan.save()
				
			insta_start += 1
			loan_amor_list.append(monthly_dict)



		#for i in loan_amor_list:
			#print (i)	
		#print(loan_amor_list)
			#print(self.payments.index(i))


		#print(len(self.payments))


		return loan_amor_list



class Amorize_on_the_spot_group(object):
	
	def __init__(self, current_loan_id):
		self.current_loan_id = current_loan_id # queryset of all payments related to the specific loan
		self.loan=self.get_loan() # this should be replaced with the loan object being operated on
		self.chart_list=[]  #cant play around with the class variables alot as its hard to play around with custom objects in django so we are stuck to istance variables
		self.decided_amount=self.get_loan_monthly_payment()
		self.ints= 0.01
		self.payments=self.get_payments()
		

	def scan_payment(self):
		decided_amount=4442.44
		if self.payment < decided_amount:
			print('underpayment')

		elif self.payment > decided_amount:
			print('overpayment')

	def process_payments(self):
		return 5000

	def get_loan(self):
		l=GroupDisbursed_Loan.objects.get(id=self.current_loan_id)
		return l


	def get_loan_monthly_payment(self):
		months=self.loan.installments
		principal=self.loan.Amount
		ints=0.01
		monthly=(ints*principal)/(1-(1+ints)**-months)   # formula for periodic payment
		return monthly



	def get_payments(self):
		l=GroupDisbursed_Loan.objects.get(id=self.current_loan_id)
		payments= loan_repayment_register_group.objects.filter(loan=l).order_by('date_payment')
		#print(payments)
		return payments

	#end of initialization sensitive methods
	
	def fetch_amorization_chart(self):
		loan_amor_list=[]
		insta_start=1
		loaned_amount=self.loan.Amount
		for i in self.payments:
			monthly_dict={}


			if insta_start == 1:
				monthly_dict['date']=i.date_payment
				monthly_dict['installment']=insta_start
				monthly_dict['amount_paid']=i.Amount
				


				#easy...
				monthly_dict['loan_balance']=loaned_amount - (i.Amount -(loaned_amount * self.ints))
				monthly_dict['interest_charged']=loaned_amount * self.ints
				
				#print( 'first')
			else:
				last_payment=loan_amor_list[len(loan_amor_list)-1]
				#print (last_payment, 'i')
				interest_charged_last=float(last_payment['loan_balance']) * self.ints
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

				if current_loan_bal == 0 or current_loan_bal < 2:
					theloan=GroupDisbursed_Loan.objects.get(id=self.loan.id)
					theloan.re_paid=True
					theloan.save()
				
			insta_start += 1
			loan_amor_list.append(monthly_dict)



		#for i in loan_amor_list:
			#print (i)	
		#print(loan_amor_list)
			#print(self.payments.index(i))


		#print(len(self.payments))


		return loan_amor_list


 

class get_individual_Loan(View):

	def get(self, request, **kwargs):
		customer=Member.objects.get(id=self.kwargs['mid'])
		c_loans=IndividualDisbursed_Loan.objects.filter(Borrower=customer)
		current_loan=IndividualDisbursed_Loan.objects.filter(Borrower=customer).filter(re_paid=False)
		
		
		if len(current_loan) != 0:

			chart=Amorize_on_the_spot(current_loan[0].id)
			
			payments=loan_repayment_register_individual.objects.filter(loan=current_loan[0])
		
		
			return render(request, 'loan_summary.html', {'loans':c_loans, 'cloan':chart.fetch_amorization_chart(),'ME':customer, 'current_loan':current_loan, 'monthly':format(chart.decided_amount, '.2f'), 'payments':len(payments), 'allpayments':payments})
		else:

			return render(request, 'loan_summary.html', {'loans':c_loans, 'ME':customer})

class get_group_Loan(View):

	def get(self, request, **kwargs):
		gcustomer=Groups.objects.get(id=self.kwargs['mid'])
		c_loans=GroupDisbursed_Loan.objects.filter(Borrower=gcustomer)
		current_loan=GroupDisbursed_Loan.objects.filter(Borrower=gcustomer).filter(re_paid=False)
		
		if len(current_loan) != 0:

			chart=Amorize_on_the_spot_group(current_loan[0].id)
			payments=loan_repayment_register_group.objects.filter(loan=current_loan[0].id)
			
			
			return render(request, 'group_loan_summary.html', {'loans':c_loans, 'cloan':chart.fetch_amorization_chart(),'ME':gcustomer, 'current_loan':current_loan, 'monthly':format(chart.decided_amount, '.2f'), 'payments':len(payments), 'allpayments':payments})
		else:

			return render(request, 'group_loan_summary.html', {'loans':c_loans, 'ME':gcustomer})


class group_loan(generics.ListCreateAPIView):
	serializer_class=group_loanSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		cstmr=Groups.objects.get(id=self.kwargs['mid'])
		queryset=GroupDisbursed_Loan.objects.filter(member=cstmr)
		
		return queryset

def get_chart(months, principal):
	installments=months

	last_installment= installments- (installments-1)
	loan_bal= []
	temp_amor_list=[]
	interest=0.01
	monthly=(interest*principal)/(1-(1+interest)**-months)   # formula for periodic payment
	
	while installments > 0:
		
		if len(loan_bal) == 0:
			interest_p=principal* 0.01
			#beore first remitance interest is charged on loan
			loan_balance=principal + interest_p - monthly

			# the monthly pay  minus the interest equals the principal amount.
			princ_amount=monthly- interest_p  #what you are paying for loans

			
			loan_bal.append((format(princ_amount, '.2f'), format(interest_p, '.2f'), format(loan_balance, '.2f')))
			temp_amor_list.append([int(installments), format(loan_balance, '.2f'), format(interest_p, '.2f'), format(monthly, '.2f')])
			installments -=1
			
			#print ((installments, format(loan_balance, '.2f'), format(interest_p, '.2f'), format(monthly, '.2f')))
		else:

			last_bal=loan_bal[len(loan_bal)-1] 
			
			interest_p=float(last_bal[2])* 0.01
			# the monthly pay  minus the interest equals the principal amount.
			princ_amount=monthly- interest_p  #what you are paying for loans

			#we then deduct the principal amount from the loan balance.
			loan_balance=float(last_bal[2]) - princ_amount
			loan_bal.append(( format(princ_amount,  '.2f'), format(interest_p,  '.2f'), format(loan_balance,  '.2f')))
			
			
			temp_amor_list.append([int(installments), format(loan_balance, '.2f'), format(interest_p, '.2f'), format(monthly, '.2f')])
			installments -=1

	#temp_amor_list[11][1]=0
	
	rev_insta=range(months)
	rev=1

	for i in temp_amor_list:

		i[0]=rev
		rev +=1
	temp_amor_list[-1][1]=0
		

	return temp_amor_list

















from datetime import timedelta

#@login_required(login_url='admin/login')
def check_defaulted_individual():
	payments=loan_repayment_register_individual.objects.all()
	all_loans=IndividualDisbursed_Loan.objects.filter()
	defaulted_loans=[]
	for i in all_loans:
		#print(i)
		#check if the loan was disbursed this month
		now=timezone.now()
	
		if i.Date_disbursment.month == now.month:
			pass

		else:
			# filtering the payments specific to each loan
			loan_payments=payments.filter(loan=i).order_by('date_payment')


			defaultdate=i.Date_disbursment + timedelta(days=60)
			
			#print(defaultdate , now)
			# less in dates means the opposite  ie.ahead of == less than   behind == greater than    print(defaultdate < now)
			if len(loan_payments) == 0 and defaultdate < now.date():
				#print('huyo', i.Date_disbursment)
				defaulted_loans.append(i)
			else:
				if len(loan_payments) == 0:
					pass
				else:

					last_payment=len(loan_payments)-1
					last=loan_payments[last_payment]
					#print(last.date_payment)
					if last.date_payment + timedelta(days=60)< now.date() :
						defaulted_loans.append(i)
	return defaulted_loans

def check_defaulted_group():
	payments=loan_repayment_register_group.objects.all()
	all_loans=GroupDisbursed_Loan.objects.filter()
	defaulted_loans=[]
	for i in all_loans:
		#print(i)
		#check if the loan was disbursed this month
		now=timezone.now()
	
		if i.Date_disbursment.month == now.month:
			pass

		else:
			# filtering the payments specific to each loan
			loan_payments=payments.filter(loan=i).order_by('date_payment')


			defaultdate=i.Date_disbursment + timedelta(days=60)
			
			#print(defaultdate , now)
			# less in dates means the opposite  ie.ahead of == less than   behind == greater than    print(defaultdate < now)
			if len(loan_payments) == 0 and defaultdate < now.date():
				#print('huyo', i.Date_disbursment)
				defaulted_loans.append(i)
			else:
				if len(loan_payments) == 0:
					pass
				else:

					last_payment=len(loan_payments)-1
					last=loan_payments[last_payment]
					#print(last.date_payment)
					if last.date_payment + timedelta(days=60)< now.date() :
						defaulted_loans.append(i)
	return defaulted_loans

		
class loansList(ListView):

	model=IndividualDisbursed_Loan
	context_object_name='loans'
	template_name='loan_analysis.html'
	def get_context_data(self, ** kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data( ** kwargs)
		# Add in a QuerySet of all the loan stats

		#repaid
		repaid_loans=IndividualDisbursed_Loan.objects.filter(re_paid=True)
		g_repaid_loans=GroupDisbursed_Loan.objects.filter(re_paid=True)
		#pending
		unsettled=IndividualDisbursed_Loan.objects.filter(re_paid=False)
		unsettled_group=GroupDisbursed_Loan.objects.filter(re_paid=False)
		#defaulted
		all_loans=IndividualDisbursed_Loan.objects.all()

		defaulters=check_defaulted_individual()
		group_defaulters=check_defaulted_group()
		customers=Member.objects.all()
	


		#assignments to context
		context['repaid'] = repaid_loans
		context['g_repaid']=g_repaid_loans
		context['pending'] = unsettled
		context['g_pending'] = unsettled_group
		context['defaulters']=defaulters
		context['g_defaulters']=group_defaulters
		context['members']=customers

		return context

class loan_register(generics.ListCreateAPIView):
	serializer_class=individual_registerSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):

		lt=Loan_tasks_base(self.kwargs['mid'], 'i')
		queryset=loan_repayment_register_individual.objects.filter(loan=lt.current_loan)

		
		return queryset

class loan_register_group(generics.ListCreateAPIView):
	serializer_class=group_registerSerializer
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):
		lt=Loan_tasks_base(self.kwargs['mid'], 'g')
		queryset=loan_repayment_register_group.objects.filter(loan=lt.current_loan)
		return queryset
	




# DEBT REALATED OPS



from .models import charges_payment_register_individual, charges_record_group, fines_record_individual, fines_record_group, charges_record_individual, charges_payment_register_individual, fines_payment_register_individual
from .serializers import charge_indi_acc, fine_indi_acc, fine_group_acc, charge_group_acc


#group debt related imports
from .forms import group_charges_payment_form, group_fines_payment_form, group_charges_record_form
from .models import charges_record_group, gshare, fines_payment_register_group, charges_payment_register_group
#class charge_individual_acc(generics.ListCreateAPIView):
	#serializer_class=charge_indi_acc
	#permission_classes= (IsAuthenticated,)
	#def get_queryset(self):
		#the_person=Member.objects.filter(id=self.kwargs['mid'])
		#charges=charges_record_individual.objects.filter(member=the_person[0]).filter(paid=False)
		
		
		#return charges


class charge_individual_acc(View):
	form_class =individual_charges_record_form
	def get(self, request, **kwargs):
		chargelist=[]
		the_person=Member.objects.filter(id=self.kwargs['mid'])
		charges=charges_record_individual.objects.filter(member=the_person[0]).filter(paid=False)
		if len(charges) == 0:
			pass
		else:
			for c in charges:
				message_objectdict={}
				message_objectdict['Date']= str(c.Date)
				message_objectdict['details']= str(c.Particulars)
				message_objectdict['Amount']=str(c.Amount_due)
				message_objectdict['pk']=str(c.pk)

			
				#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
				chargelist.append(message_objectdict)
			
		return HttpResponse(json.dumps(chargelist), content_type="application/json")

	def post(self, request, **kwargs):
		
		new_data=request.POST
		
		#print(len(GS))
		form = self.form_class(new_data)
		if form.is_valid():
			unsaved_form=form.save(commit=False)

			unsaved_form.save()	
			
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			#print(form.errors.as_json()) how you can pass errors back to the frontend
			return HttpResponse('FAILED')


class charge_group_acc(View):
	form_class =group_charges_record_form
	def get(self, request, **kwargs):
		chargelist=[]
		the_group=Groups.objects.filter(id=self.kwargs['mid'])
		charges=charges_record_group.objects.filter(group=the_group[0]).filter(paid=False)
		if len(charges) == 0:
			pass
		else:
			for c in charges:
				message_objectdict={}
				message_objectdict['Date']= str(c.Date)
				message_objectdict['details']= str(c.Particulars)
				message_objectdict['Amount']=str(c.Amount_due)
				message_objectdict['pk']=str(c.pk)

			
				#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
				chargelist.append(message_objectdict)
			
		return HttpResponse(json.dumps(chargelist), content_type="application/json")

	def post(self, request, **kwargs):
		
		new_data=request.POST
		
		#print(len(GS))
		form = self.form_class(new_data)
		print(form.is_valid())
		if form.is_valid():
			unsaved_form=form.save(commit=False)

			unsaved_form.save()	
			
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json()) #how you can pass errors back to the frontend
			return HttpResponse('FAILED')	


class fine_individual_acc(generics.ListCreateAPIView):
	serializer_class=fine_indi_acc
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):
		the_person=Member.objects.get(id=self.kwargs['mid'])
		fines=fines_record_individual.objects.filter(member=the_person).filter(paid=False)
		
		
		return fines

class fine_group_acc(generics.ListCreateAPIView):
	serializer_class=fine_group_acc
	permission_classes= (IsAuthenticated,)
	def get_queryset(self):
		the_group=Groups.objects.get(id=self.kwargs['mid'])
		fines=fines_record_group.objects.filter(group=the_group).filter(paid=False)
		
		
		return fines



class individual_charge(View):

	
	def get(self, request):
		charges=charges_record_individual.objects.filter()

		for c in text:
			message_objectdict={}
			
			message_objectdict['name']= str(c.name)
			message_objectdict['membership_no']=str(c.membership_no)
			message_objectdict['pk']=str(c.pk)
		
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")

class pay_charges_individual(View):
	form_class=individual_charges_payment_form
	def post(self, request, * args, **kwargs):
		new_data=request.POST
		charges=request.POST['charges'].split(',')
		amount_charge=0
		for i in charges:
			the_charge=charges_record_individual.objects.get(id=i)
			amount_charge += the_charge.Amount_due

		
	
		#print(new_data['Amount'])
		form = self.form_class(new_data)
		
		if form.is_valid():
		
			if amount_charge > int(new_data['Amount']):
			
				return HttpResponse('insufficient_funds')	
			unsaved_form=form.save(commit=False)
		
			for i in charges:
				the_charge=charges_record_individual.objects.get(id=i)
				the_charge.paid=True
				the_charge.save()
				unsaved_form.charge.add(i)
			unsaved_form.save()	
			#print(unsaved_form.gurantor, 'hakuna ama?')
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json())
			return HttpResponse('FAILED')
class pay_charges_group(View):
	form_class=group_charges_payment_form
	def post(self, request, * args, **kwargs):
		new_data=request.POST
		charges=request.POST['charges'].split(',')
		amount_charge=0
		for i in charges:
			the_charge=charges_record_group.objects.get(id=i)
			amount_charge += the_charge.Amount_due

		
	
		#print(new_data['Amount'])
		form = self.form_class(new_data)
		
		if form.is_valid():
		
			if amount_charge > int(new_data['Amount']):
			
				return HttpResponse('insufficient_funds')
			unsaved_form=form.save(commit=False)
		
			for i in charges:
				the_charge=charges_record_group.objects.get(id=i)
				the_charge.paid=True
				the_charge.save()
				unsaved_form.charge.add(i)
			unsaved_form.save()	
			#print(unsaved_form.gurantor, 'hakuna ama?')
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json())
			return HttpResponse('FAILED')



class pay_fines_individual(View):
	form_class=individual_fines_payment_form
	def post(self, request, * args, **kwargs):
		new_data=request.POST
		fines=request.POST['fines'].split(',')
		amount_fine=0
		for i in fines:
			the_fine=fines_record_individual.objects.get(id=i)
			amount_fine += the_fine.Amount_due


		form = self.form_class(new_data)
		
		if form.is_valid():
			if amount_fine > int(new_data['Amount']):
			
				return HttpResponse('insufficient_funds')
			unsaved_form=form.save(commit=False)
			print(unsaved_form)
			for i in fines:
				the_fine=fines_record_individual.objects.get(id=i)
				the_fine.paid=True
				the_fine.save()
				unsaved_form.fine.add(i)
			unsaved_form.save()	
			#print(unsaved_form.gurantor, 'hakuna ama?')
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json())
			return HttpResponse('FAILED')



class pay_fines_group(View):
	form_class=group_fines_payment_form
	def post(self, request, * args, **kwargs):
		new_data=request.POST
		fines=request.POST['fines'].split(',')
		amount_fine=0
		for i in fines:
			the_fine=fines_record_group.objects.get(id=i)
			amount_fine += the_fine.Amount_due


		form = self.form_class(new_data)
		
		if form.is_valid():
			if amount_fine > int(new_data['Amount']):
			
				return HttpResponse('insufficient_funds')
			unsaved_form=form.save(commit=False)
			print(unsaved_form)
			for i in fines:
				the_fine=fines_record_group.objects.get(id=i)
				the_fine.paid=True
				the_fine.save()
				unsaved_form.fine.add(i)
			unsaved_form.save()	
			#print(unsaved_form.gurantor, 'hakuna ama?')
			return HttpResponse('success')
			#print(request.POST['gurantor'].split(','))
		else:
			form = self.form_class(new_data)
			print(form.errors.as_json())
			return HttpResponse('FAILED')





# PDF OPS


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import red, green
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.graphics.shapes import *

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
from reportlab.pdfbase.ttfonts import TTFont


@login_required(login_url='admin/login')
def shares_pdf(request, shares_id):
	cstmr=Member.objects.get(id=shares_id)
	c_loan=IndividualDisbursed_Loan.objects.filter(Borrower=cstmr).filter(re_paid=False)
	if len(c_loan) != 0:
		loan_payment_today=loan_repayment_register_individual.objects.filter(date_payment=timezone.now().date()).filter(loan=c_loan[0])
	else:
		loan_payment_today=[]
	#print(loan_payment_today)

	mem=Member.objects.get(id=shares_id)	
	
	shares_today=Share.objects.filter(member=mem).filter(date_payment=timezone.now().date())
	#print(shares_today)
	charges=charges_record_individual.objects.filter(member=mem)
	fines=fines_record_individual.objects.filter(member=mem)
	total=0
	
	allcharges_payments=[]
	allfines_payments=[]
	todays_charges_payments=[]
	todays_fines_payments=[]
	
	for i in charges:

		charges_payments=charges_payment_register_individual.objects.filter(charge=i)

		allcharges_payments.append(charges_payments)

	for i in fines:

		fines_payments=fines_payment_register_individual.objects.filter(fine=i)
		allfines_payments.append(fines_payments)

	for i in allfines_payments:
		for a in i:
			if (a.date_payment == timezone.now().date()):
				todays_fines_payments.append(a)
				total +=a.Amount

	for i in allcharges_payments:
		for a in i:
			if (a.date_payment == timezone.now().date()):
				todays_charges_payments.append(a)
				total +=a.Amount
	

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="sharesreceipt.pdf" '
	buffer = BytesIO()
	c = canvas.Canvas(response)
	bogustext = ("JIENDELEZE SELF HELP GROUP ") 
	c.setTitle('receipt')
	c.setPageSize((60 * mm, 79 * mm))
	c.setFont('VeraBd', 9)
	c.drawString(10, 210, bogustext)
	c.setFont('VeraBd', 7)
	c.drawString(30, 200, "P.O. BOX 23068, Lower Kabete")
	c.setFont('Vera', 8)
	c.drawString(5, 185, "DATE:")


	c.setFont('VeraBI', 8)
	c.drawString(35, 185, str(timezone.now().date()))

	c.setFont('Vera', 8)
	c.drawString(5, 170, "NAME:")

	c.setFont('VeraBI', 8)
	c.drawString(35, 170, str(mem))

	c.setFont('Vera', 8)
	c.drawString(5, 150, "MEMBERSHIP NO:")

	c.setFont('VeraBI', 8)
	c.drawString(80, 150, mem.membership_no)
	c.line(0, 140, 590, 140) #top line
	c.setFont('VeraBd', 8)
	y=120
	x=120

	for i in todays_charges_payments:
		y-=10
		c.drawString(10, y, str(i.charge.all()[0].Particulars))
		c.drawString(x, y, str(i.charge.all()[0].Amount_due))
		

	for i in todays_fines_payments:
		y-=10
		c.drawString(10, y, str(i.fine.all()[0].Particulars))
		c.drawString(x, y, str(i.fine.all()[0].Amount_due))

	for i in shares_today:
		y-=10
		c.drawString(10, y, str("Shares "))
		c.drawString(x, y, str(i.Amount))
		total+=i.Amount

	for i in loan_payment_today:
		y-=10
		c.drawString(10, y, str("Loan payment "))
		c.drawString(x, y, str(i.Amount))
		total+=i.Amount
		
	y-=20
	c.drawString(10, y, "TOTAL: ")
	c.drawString(x, y, str(total))
	c.setFont('Vera', 8)
	c.drawString(5, 130, "PARTICULARS:")
	#c.drawString(5, 90, "AMOUNT:")

	c.setFont('VeraBI', 8)
	

	
	c.showPage()
	c.save()
	return response



@login_required(login_url='admin/login')
def shares_pdf_group(request, shares_id):
	
	mem=Groups.objects.get(id=shares_id)
	
	c_loan=GroupDisbursed_Loan.objects.filter(Borrower=mem).filter(re_paid=False)
	if len(c_loan) != 0:
		loan_payment_today=loan_repayment_register_group.objects.filter(date_payment=timezone.now().date()).filter(loan=c_loan[0])
	else:
		loan_payment_today=[]
	shares_today=gshare.objects.filter(group=mem).filter(date_payment=timezone.now().date())
	#print(shares_today)
	charges=charges_record_group.objects.filter(group=mem)
	fines=fines_record_group.objects.filter(group=mem)
	total=0
	
	allcharges_payments=[]
	allfines_payments=[]
	todays_charges_payments=[]
	todays_fines_payments=[]
	
	for i in charges:

		charges_payments=charges_payment_register_group.objects.filter(charge=i)

		allcharges_payments.append(charges_payments)

	for i in fines:

		fines_payments=fines_payment_register_group.objects.filter(fine=i)
		allfines_payments.append(fines_payments)

	for i in allfines_payments:
		for a in i:
			if (a.date_payment == timezone.now().date()):
				todays_fines_payments.append(a)
				total +=a.Amount

	for i in allcharges_payments:
		for a in i:
			if (a.date_payment == timezone.now().date()):
				todays_charges_payments.append(a)
				total +=a.Amount

	

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="sharesreceipt.pdf" '
	buffer = BytesIO()
	c = canvas.Canvas(response)
	bogustext = ("JIENDELEZE SELF HELP GROUP ") 
	c.setTitle('receipt')
	c.setPageSize((60 * mm, 79 * mm))
	c.setFont('VeraBd', 9)
	c.drawString(10, 210, bogustext)
	c.setFont('VeraBd', 7)
	c.drawString(30, 200, "P.O. BOX 23068, Lower Kabete")
	c.setFont('Vera', 8)
	c.drawString(5, 185, "DATE:")


	c.setFont('VeraBI', 8)
	c.drawString(35, 185, str(timezone.now().date()))

	c.setFont('Vera', 8)
	c.drawString(5, 170, "NAME:")

	c.setFont('VeraBI', 8)
	c.drawString(35, 170, str(mem))

	c.setFont('Vera', 8)
	c.drawString(5, 150, "MEMBERSHIP NO:")

	c.setFont('VeraBI', 8)
	c.drawString(80, 150, mem.membership_no)
	c.line(0, 140, 590, 140) #top line
	c.setFont('VeraBd', 8)
	y=120
	x=120

	for i in todays_charges_payments:
		y-=10
		c.drawString(10, y, str(i.charge.all()[0].Particulars))
		c.drawString(x, y, str(i.charge.all()[0].Amount_due))
		

	for i in todays_fines_payments:
		y-=10
		c.drawString(10, y, str(i.fine.all()[0].Particulars))
		c.drawString(x, y, str(i.fine.all()[0].Amount_due))

	for i in shares_today:
		y-=10
		c.drawString(10, y, str("Shares "))
		c.drawString(x, y, str(i.Amount))
		total+=i.Amount

	for i in loan_payment_today:
		y-=10
		c.drawString(10, y, str("Loan payment "))
		c.drawString(x, y, str(i.Amount))
		total+=i.Amount
		
	y-=20
	c.drawString(10, y, "TOTAL: ")
	c.drawString(x, y, str(total))
	c.setFont('Vera', 8)
	c.drawString(5, 130, "PARTICULARS:")
	#c.drawString(5, 90, "AMOUNT:")

	c.setFont('VeraBI', 8)
	

	
	c.showPage()
	c.save()
	return response





@login_required(login_url='admin/login')
def loans_payment_individual_pdf(request, loan_id):

	form=loan_repayment_register_individual.objects.get(id=loan_id)
	loan=form.loan
	no_payments=len(loan_repayment_register_individual.objects.filter(loan=loan))

	#fine=fines_record_individual.objects.get(id=form.fine.id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="LoanRepaymentReceipt.pdf" '
	buffer = BytesIO()
	c = canvas.Canvas(response)
	bogustext = ("JIENDELEZE SELF HELP GROUP ") 
	c.setTitle('receipt')
	c.setPageSize((60 * mm, 79 * mm))
	c.setFont('VeraBd', 9)
	c.drawString(10, 210, bogustext)
	c.setFont('VeraBd', 7)
	c.drawString(30, 200, "P.O. BOX 23068, Lower Kabete")
	c.setFont('Vera', 8)
	c.drawString(5, 180, "DATE:")

	c.setFont('VeraBI', 8)
	c.drawString(35, 180, str(form.date_payment))

	c.setFont('Vera', 8)
	c.drawString(5, 160, "NAME:")


	c.setFont('VeraBd', 8)
	c.drawString(35, 160, str(loan.Borrower))

	c.setFont('Vera', 8)
	c.drawString(5, 150, "MEMBERSHIP NO:")


	c.setFont('VeraBd', 8)
	c.drawString(80, 150, str(loan.Borrower.membership_no))

	c.line(5, 140, 165, 140) #top line
	c.setFont('VeraBd', 8)
	
	c.drawString(70, 120, "LOAN PAYMENT")
	c.setFont('Vera', 8)

	c.drawString(5, 120, "PARTICULARS:")
	c.drawString(5, 90, "Amount:")


	c.setFont('VeraBI', 8)
	c.drawString(50, 90, str(form.Amount))

	c.setFont('Vera', 8)
	c.drawString(5, 70, "Installment:")

	c.setFont('VeraBI', 8)
	c.drawString(70, 70, str(no_payments))


	c.setFont('Vera', 8)
	c.drawString(100, 70, "of:")


	c.setFont('VeraBI', 8)
	c.drawString(130, 70, str(loan.installments))


	c.showPage()
	c.save()
	return response

@login_required(login_url='admin/login')
def loans_payment_group_pdf(request, loan_id):

	form=loan_repayment_register_group.objects.get(id=loan_id)
	loan=form.loan
	no_payments=len(loan_repayment_register_group.objects.filter(loan=loan))

	#fine=fines_record_individual.objects.get(id=form.fine.id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="LoanRepaymentReceipt.pdf" '
	buffer = BytesIO()
	c = canvas.Canvas(response)
	bogustext = ("JIENDELEZE SELF HELP GROUP ") 
	c.setTitle('receipt')
	c.setPageSize((60 * mm, 79 * mm))
	c.setFont('VeraBd', 9)
	c.drawString(10, 210, bogustext)
	c.setFont('VeraBd', 7)
	c.drawString(30, 200, "P.O. BOX 23068, Lower Kabete")
	c.setFont('Vera', 8)
	c.drawString(5, 180, "DATE:")

	c.setFont('VeraBI', 8)
	c.drawString(35, 180, str(form.date_payment))

	c.setFont('Vera', 8)
	c.drawString(5, 160, "NAME:")


	c.setFont('VeraBd', 8)
	c.drawString(35, 160, str(loan.Borrower))

	c.setFont('Vera', 8)
	c.drawString(5, 150, "MEMBERSHIP NO:")


	c.setFont('VeraBd', 8)
	c.drawString(80, 150, str(loan.Borrower.membership_no))

	c.line(5, 140, 165, 140) #top line
	c.setFont('VeraBd', 8)
	
	c.drawString(70, 120, "LOAN PAYMENT")
	c.setFont('Vera', 8)

	c.drawString(5, 120, "PARTICULARS:")
	c.drawString(5, 90, "Amount:")


	c.setFont('VeraBI', 8)
	c.drawString(50, 90, str(form.Amount))

	c.setFont('Vera', 8)
	c.drawString(5, 70, "Installment:")

	c.setFont('VeraBI', 8)
	c.drawString(70, 70, str(no_payments))


	c.setFont('Vera', 8)
	c.drawString(100, 70, "of:")


	c.setFont('VeraBI', 8)
	c.drawString(130, 70, str(loan.installments))


	c.showPage()
	c.save()
	return response


