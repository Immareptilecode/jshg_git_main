"""jiendeleze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')add_shares
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Membership.views import MembersList, clist,clist_loansearch, glist, GroupList, Member_info, Group_info, glist_loansearch, clist_loansearch_application, glist_loansearch_app
from Membership.apiviews import CustomerList, customersearch
from Finance.views import shareslist, Groupshareslist, loansList, individual_loan, group_loan, processLoan, processLoan_group, get_chart, get_individual_Loan,  loan_register, loan_register_group, get_group_Loan, shares_pdf 
from Reports.views import Reports_home, charges_reports, fines_reports, loan_reports

#debt views

from Finance.views import charge_individual_acc, charge_group_acc, fine_individual_acc, fine_group_acc, pay_charges_individual, pay_fines_individual, pay_charges_group, pay_fines_group, loans_payment_individual_pdf, loans_payment_group_pdf, shares_pdf_group
from django.contrib.auth.decorators import login_required

# Share capital views

from Finance.views import shareCapital_individual, shareCapital_group, calculate_shares, calculate_sharecapital, calculate_sharecapitalGroup, calculate_shares_group


#loan offset views

from Finance.views import offsetloan_individual, offsetloan_group 

urlpatterns = [
    path('admin/', admin.site.urls, name='ad'),
   	

    path('', login_required(login_url='admin/login')(MembersList.as_view()) , name='customerslist'),
    path('customers', login_required(login_url='admin/login')(CustomerList.as_view()), name='customers'),
    path('Groups', login_required(login_url='admin/login')(GroupList.as_view()), name='groups'),
    path('customerslst/', login_required(login_url='admin/login')(clist.as_view()), name="customerlist"),
    path('customerslst loan/', login_required(login_url='admin/login')(clist_loansearch.as_view()), name="customerlistloan"),
    path('customerslst loan application/', login_required(login_url='admin/login')(clist_loansearch_application.as_view()), name="customerlistloan_app"),
    path('Grouplst loan/', login_required(login_url='admin/login')(glist_loansearch.as_view()), name="grouplistloan"),
    path('Grouplst loan application/', login_required(login_url='admin/login')(glist_loansearch_app.as_view()), name="grouplistloan_app"),
    path('groupslst/', login_required(login_url='admin/login')(glist.as_view()), name="grouplist"),
    path('<uuid:pk>', Member_info.as_view(), name="memberdetail"),
    path('group/<uuid:pk>', Group_info.as_view(), name='groupdetail'),




    #Shares

    path('cshares/<uuid:mid>', shareslist.as_view(), name='addshares'),
    path('gshares/<uuid:mid>', Groupshareslist.as_view(), name='group_addshares'),
    path('individual calculate shares/<uuid:mid>', login_required(login_url='admin/login')(calculate_shares.as_view()), name='get_shares_individual'),
    path('group calculate shares/<uuid:mid>', login_required(login_url='admin/login')(calculate_shares_group.as_view()), name='get_shares_group'),

    #Share Capital
    path('shareCapital/<uuid:mid>', shareCapital_individual.as_view(), name='addsharecapital'),
    path('GoupshareCapital/<uuid:mid>', shareCapital_group.as_view(), name='group_addsharecapital'),
    path('getIndividualShareCapital/<uuid:mid>', login_required(login_url='admin/login')(calculate_sharecapital.as_view()), name='TotalIndividual_sharecapital'),
    path('getGroupShareCapital/<uuid:mid>', login_required(login_url='admin/login')(calculate_sharecapitalGroup.as_view()), name='TotalGroup_sharecapital'),


    



    #loans

    path('Loans', login_required(login_url='admin/login')(loansList.as_view()) , name='loans'),
    path('loansummary/<uuid:mid>', get_individual_Loan.as_view(), name='loan_summary'),
    path('grouploansummary/<uuid:mid>', get_group_Loan.as_view(), name='loan_summary_group'),
    path('processLoan/<int:mid>', login_required(login_url='admin/login')(processLoan.as_view()), name='applyloan'),
    path('process group Loan/<int:mid>', login_required(login_url='admin/login')(processLoan_group.as_view()), name='applyloan_group'),
    path('amorization/<int:months>/<int:principal', get_chart, name="amor_chart"),
    path('loanregister/<uuid:mid>', loan_register.as_view(), name="loan_register"),
    path('loanregistergroup/<uuid:mid>', loan_register_group.as_view(), name="loan_register_group"),
    path('offset loan individual/<uuid:mid>/<str:loan_balance>',  login_required(login_url='admin/login')(offsetloan_individual.as_view()), name="offsetLoan_individual"),
    path('offset loan group/<uuid:mid>/<str:loan_balance>',  login_required(login_url='admin/login')(offsetloan_group.as_view()), name="offsetLoan_group"),
    

    #debts

    path('charge individual/<uuid:mid>', login_required(login_url='admin/login')(charge_individual_acc.as_view()), name="charge_individual"),
    path('charge group/<uuid:mid>', login_required(login_url='admin/login')(charge_group_acc.as_view()), name="charge_group"),
    path('Fine individual/<uuid:mid>', fine_individual_acc.as_view(), name="fine_individual"),
    path('Fine group/<uuid:mid>', fine_group_acc.as_view(), name="fine_group"),

    path('paycharges', login_required(login_url='admin/login')(pay_charges_individual.as_view()), name="paycharges_individual"),
    path('payfines', login_required(login_url='admin/login')(pay_fines_individual.as_view()), name="payfines_individual"),
    path('paycharges group', login_required(login_url='admin/login')(pay_charges_group.as_view()), name="paycharges_group"),
    path('payfines group', login_required(login_url='admin/login')(pay_fines_group.as_view()), name="payfines_group"),


    #reports


    path('Reports Home', login_required(login_url='admin/login')(Reports_home.as_view()), name='reportshome'),
    path('get charges/<int:year>/<int:month>/<int:day>', login_required(login_url='admin/login')(charges_reports.as_view()), name="fetch_charges_report"), 
    path('get fines/<int:year>/<int:month>/<int:day>', login_required(login_url='admin/login')(fines_reports.as_view()), name="fetch_fines_report"), 
    path('get loans/<int:year>/<int:month>/<int:day>', login_required(login_url='admin/login')(loan_reports.as_view()), name="fetch_loans_report"), 
    




    #pdfs

    path('sharespdf/<uuid:shares_id>', shares_pdf, name='sharespdf'),
    path('sharespdfg/<uuid:shares_id>', shares_pdf_group, name='sharespdfgroup'),
    path('loanspdf/<uuid:loan_id>', loans_payment_individual_pdf, name="loan_pdf_indi"),
    path('loanspdfg/<uuid:loan_id>', loans_payment_group_pdf, name="loan_pdf_grp")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)