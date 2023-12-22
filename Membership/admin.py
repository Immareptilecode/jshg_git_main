from django.contrib import admin
from .models import Member, Groups
from django.contrib.auth.models import Group
# Register your models here.
class MembershipAdmin(admin.ModelAdmin):
	
	list_display =('Member_photo','first_name','last_name', 'membership_no')


class GroupAdmin(admin.ModelAdmin):
	
	list_display =('name', 'membership_no')
	
admin.site.register(Member, MembershipAdmin)
admin.site.unregister(Group)
admin.site.register(Groups, GroupAdmin)



