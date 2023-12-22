from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views import static
from.models import Member, Groups
# Create your views here.
from django.http import JsonResponse
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from Finance.models	import Share
class glist(View):

	
	def get(self, request):

		text=Groups.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['name']= str(c.name)
			message_objectdict['membership_no']=str(c.membership_no)
			message_objectdict['pk']=str(c.pk)
			message_objectdict['url']='group/%s ' % str(c.pk)
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")


class clist(View):

	
	def get(self, request):

		text=Member.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['fname']= str(c.first_name)
			message_objectdict['membership_no']= str(c.membership_no)
			message_objectdict['lname']=str(c.last_name)
			message_objectdict['pk']=str(c.pk)
			message_objectdict['url']= str(c.pk)
			if c.photo:
				message_objectdict['img']=c.photo.url# production
			else:
				print('no pic')
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")


class clist_loansearch(View):

	
	def get(self, request):

		text=Member.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['fname']= str(c.first_name)
			message_objectdict['membership_no']= str(c.membership_no)
			message_objectdict['lname']=str(c.last_name)
			message_objectdict['pk']=str(c.pk)
			message_objectdict['url']='loansummary/%s' % str(c.pk)
			message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")

class clist_loansearch_application(View):

	
	def get(self, request):

		text=Member.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['fname']= str(c.first_name)
			message_objectdict['membership_no']= str(c.membership_no)
			message_objectdict['lname']=str(c.last_name)
			message_objectdict['pk']=str(c.pk)
			
			message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")
 
class glist_loansearch(View):

	
	def get(self, request):

		text=Groups.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['name']= str(c.name)
			message_objectdict['membership_no']=str(c.membership_no)
			message_objectdict['pk']=str(c.pk)
			message_objectdict['url']='grouploansummary/%s' % str(c.pk)
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")

class glist_loansearch_app(View):

	
	def get(self, request):

		text=Groups.objects.all()
		#n_pages=serializers.serialize("json", text) 
	
		message_dict_forjs=[]
		
		#print (text[len(text)-1].pk)

		for c in text:
			message_objectdict={}
			
			message_objectdict['name']= str(c.name)
			message_objectdict['membership_no']=str(c.membership_no)
			message_objectdict['pk']=str(c.pk)
		
			#message_objectdict['img']='media/%s '% str(c.photo )  #static( c.photo )) production
			message_dict_forjs.append(message_objectdict)
				
			


		return HttpResponse(json.dumps(message_dict_forjs), content_type="application/json")




class MembersList(ListView):

	model=Member
	context_object_name='customers'
	template_name='customer_analysis.html'

class GroupList(ListView):
	model=Groups
	context_object_name='group_customers'
	template_name='group_analysis.html'

from Finance.models import charges_record_individual, charges_payment_register_individual, fines_record_individual, fines_payment_register_individual, gshare, charges_record_group, fines_record_group, charges_payment_register_group, fines_payment_register_group
from Finance.models import IndividualDisbursed_Loan, GroupDisbursed_Loan
from Finance.views import Amorize_on_the_spot, Amorize_on_the_spot_group


class Member_info(LoginRequiredMixin, DetailView):
	queryset=Member.objects.all()
	context_object_name = 'member'
	template_name='memberdetail.html'
	login_url = 'admin/login/'
	def get_context_data(self, ** kwargs):
		charges_payments=[]
		fines_payments=[]
		unassigned_fines=[]
		doublepayed_charges=[]
		unassigned_charges=[]
		doublepayed_fines=[]
		c=Share.objects.filter(member=self.kwargs['pk']).order_by('-date_payment')[:7]
		cstmr=Member.objects.get(id=self.kwargs['pk'])
		#here the only sorting that can be enforced is at this level as we have no controll over the append part of the loop
		# and neither can we alter the order of the payments based on the date 

		#so we fetch the three most recent debts and use them to fetch their respective paymments in the loops below
		#the list of payments comprises of querysets

		#the point is to provide the most probably required receipts for printing which would be none other than our three recent payments

		charges=charges_record_individual.objects.filter(member=self.kwargs['pk']).filter(paid=True).order_by('-Date')[:7]
		fines=fines_record_individual.objects.filter(member=self.kwargs['pk']).filter(paid=True).order_by('-Date')[:7]
		charges_to_work_with=charges_record_individual.objects.filter(member=self.kwargs['pk']).filter(paid=True)
		fines_to_work_with=fines_record_individual.objects.filter(member=self.kwargs['pk']).filter(paid=True)

		c_loan=IndividualDisbursed_Loan.objects.filter(Borrower=cstmr).filter(re_paid=False)
		if len(c_loan) != 0:

			chart=Amorize_on_the_spot(c_loan[0].id)
			amor_table=chart.fetch_amorization_chart()

			if len(amor_table) < 2 and len(amor_table) != 0: #checks for a sngle payment
				last_payment=amor_table[len(amor_table)-1]

				loan_balance=last_payment['loan_balance']
			elif len(amor_table) > 1:    #checks for multiple payments

				last_payment=amor_table[len(amor_table)-1]
				loan_balance=last_payment['loan_balance']
			elif len(amor_table) == 0: #checks for no payments at all
				loan_balance=c_loan[0].Amount
		else:
			#if member has no loan
			loan_balance=0



		for i in charges_to_work_with:
			#error catching for double payments

			try:
				paid_charges=charges_payment_register_individual.objects.get(charge=i)
			except charges_payment_register_individual.MultipleObjectsReturned:
				doublepayed_charges.append(i)
			except charges_payment_register_individual.DoesNotExist:
				unassigned_charges.append(i)
			else:
				charges_payments.append(paid_charges)

		
				
		
		for i in fines_to_work_with:
			#error catching for unassigned payments
			try:
				paid_fines=fines_payment_register_individual.objects.get(fine=i)

			except fines_payment_register_individual.MultipleObjectsReturned:
                                doublepayed_fines.append(i)
			except fines_payment_register_individual.DoesNotExist:
				unassigned_fines.append(i)

			else:
				fines_payments.append(paid_fines)
		
		context = super().get_context_data( ** kwargs)
		#repaid_loans=IndividualDisbursed_Loan.objects.filter(re_paid=True)
		context['current_loan']=c_loan
		context['shares'] = c
		context['charges_payments'] = charges_payments
		context['fines_payments'] = fines_payments
		
		context['loan_balance']=loan_balance
		return context

class Group_info(LoginRequiredMixin, DetailView):
	queryset=Groups.objects.all()
	context_object_name = 'group'
	template_name='groupdetail.html'
	login_url = 'admin/login/'

	def get_context_data(self, ** kwargs):
		charges_payments=[]
		fines_payments=[]
		unassigned_fines=[]
		doublepayed_charges=[]
		c=gshare.objects.filter(group=self.kwargs['pk']).order_by('-date_payment')[:7]
		cstmr=Groups.objects.get(id=self.kwargs['pk'])
		c_loan=GroupDisbursed_Loan.objects.filter(Borrower=cstmr).filter(re_paid=False)
		
		if len(c_loan) != 0:

			chart=Amorize_on_the_spot_group(c_loan[0].id)
			amor_table=chart.fetch_amorization_chart()
		
			if len(amor_table) < 2 and len(amor_table) != 0: #checks for a sngle payment
				last_payment=amor_table[len(amor_table)-1]

				loan_balance=last_payment['loan_balance']
			elif len(amor_table) > 1:    #checks for multiple payments

				last_payment=amor_table[len(amor_table)-1]
				loan_balance=last_payment['loan_balance']
			elif len(amor_table) == 0: #checks for no payments at all
				loan_balance=c_loan[0].Amount
		else:
			#if member has no loan
			loan_balance=0

		#here the only sorting that can be enforced is at this level as we have no controll over the append part of the loop
		# and neither can we alter the order of the payments based on the date 

		#so we fetch the three most recent debts and use them to fetch their respective paymments in the loops below
		#the list of payments comprises of querysets

		#the point is to provide the most probably required receipts for printing which would be none other than our three recent payments

		charges=charges_record_group.objects.filter(group=self.kwargs['pk']).filter(paid=True).order_by('-Date')[:7]
		fines=fines_record_group.objects.filter(group=self.kwargs['pk']).filter(paid=True).order_by('-Date')[:7]
		for i in charges:
			
			
			try:
				paid_charges=charges_payment_register_group.objects.get(charge=i)
			except charges_payment_register_group.MultipleObjectsReturned:
				doublepayed_charges.append(i)
			else:
				charges_payments.append(paid_charges)
		

		for i in fines:
			
			
			try:
				paid_fines=fines_payment_register_group.objects.get(fine=i)
			except fines_payment_register_group.DoesNotExist:
				unassigned_fines.append(i)

			else:
				fines_payments.append(paid_fines)
		
		context = super().get_context_data( ** kwargs)
		#repaid_loans=IndividualDisbursed_Loan.objects.filter(re_paid=True)
		context['current_loan']=c_loan
		context['shares'] = c
		context['charges_payments'] = charges_payments
		context['fines_payments'] = fines_payments
		context['loan_balance']=loan_balance
		return context
	




