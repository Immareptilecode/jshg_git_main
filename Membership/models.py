from django.db import models
import uuid
from django.utils.safestring import mark_safe
from django.utils import timezone	

female='F'
male='M'


GENDER_CHOICES = (
(male, 'male'),
(female, 'female'),

)


from django.templatetags.static import static

# Create your models here.
class Member(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	first_name=models.CharField(max_length=30, blank=False, verbose_name='First Name:')
	surname=models.CharField(max_length=30, blank=False, verbose_name='Surname:')
	last_name=models.CharField(max_length=30, blank=False, verbose_name='Last Name:')
	photo=models.ImageField(upload_to='members_photos', blank=True)
	sex=models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default=female)	
	id_no=models.CharField(max_length=10, blank=True, verbose_name='ID No')
	date_of_birth=models.DateField(blank=True, verbose_name='DATE OF BIRTH')
	phone_no=models.CharField(max_length=10, unique=False, blank=True, verbose_name='Phone number.')
	phone_no2=models.CharField(max_length=10, unique=False, blank=True, verbose_name='Alternate phone number.')
	email=models.CharField(max_length=40, blank=True)
	occupation=models.CharField(max_length=35, blank=True)
	county=models.CharField(max_length=35, blank=True, verbose_name='PLACE OF BIRTH: County')
	subcounty=models.CharField(max_length=35, blank=True, verbose_name='PLACE OF BIRTH: Sub County')
	ward=models.CharField(max_length=35, blank=True, verbose_name='PLACE OF BIRTH: Ward')
	village=models.CharField(max_length=35, blank=True, verbose_name='PLACE OF BIRTH: Village')
	membership_no=models.CharField(max_length=35, unique=True, verbose_name='Membership No')
	residence=models.CharField(max_length=35, blank=True,  verbose_name='Current place of Residence.')

	join_date=models.DateField(blank=False, default=timezone.now)

	Bank=models.CharField(max_length=30, blank=True)
	Branch=models.CharField(max_length=30, blank=True)
	ac_no=models.CharField(max_length=30, blank=True)

	nok_name=models.CharField(max_length=30, verbose_name='NEXT OF KIN.  Name:', blank=True)
	nok_relationship=models.CharField(max_length=30, verbose_name='NEXT OF KIN.  Relationship:', blank=True)
	nok_id=models.CharField(max_length=30, verbose_name='NEXT OF KIN.  Id No /Birth Certificate:', blank=True)

	beneficiaries=models.TextField(max_length=50, blank=True)

	def __str__(self):
		if self.sex == 'M':
			template = 'MR {0.first_name} {0.last_name}'
		elif self.sex =='F':
			template = 'MRS/MISS {0.first_name} {0.last_name}'
		return template.format(self)


	def Member_photo(self):
		if self.photo:
			return mark_safe('<img src="%s" style="width:150px; height:100px;" />' % self.photo.url)
		else:
			if self.sex == 'M':

				return 'No Image Found'


class Groups(models.Model):
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name=models.CharField(max_length=50, blank=False)
	membership_no=models.CharField(max_length=10)
	date_join=models.DateField(default=timezone.now)
	def __str__(self):

		return self.name


	class Meta:
		verbose_name = 'Group'
		verbose_name_plural = 'Groups'

class Groups_extra_details(models.Model):	  
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	group=models.ForeignKey(Groups, on_delete=models.CASCADE, blank=False)
	chairman_name=models.CharField(max_length=50, blank=False)
	secretary_name=models.CharField(max_length=50, blank=False)
	treasurer_name=models.CharField(max_length=50, blank=False)
	chairman_id=models.IntegerField(blank=False)
	secretary_id=models.IntegerField(blank=False)
	treasurer_id=models.IntegerField(blank=False)
	postal_address=models.CharField(max_length=30)
	phone=models.CharField(max_length=10)

	county=models.CharField(max_length=35, blank=True, verbose_name='Physical Address: County')
	subcounty=models.CharField(max_length=35, blank=True, verbose_name='Physical Address: Sub County')
	ward=models.CharField(max_length=35, blank=True, verbose_name='Physical Address: Ward')
	village=models.CharField(max_length=35, blank=True, verbose_name='Physical Address: Village')

	Bank=models.CharField(max_length=30, blank=True)
	ac_name=models.CharField(max_length=30, blank=True)
	ac_no=models.CharField(max_length=30, blank=True)

	class Meta:
		verbose_name = 'Group detail'
		verbose_name_plural = 'Group       details'


