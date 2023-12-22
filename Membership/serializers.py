from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):

	class Meta:
		model = Member
		fields= ('date_of_birth', 'sex', 'first_name', 'last_name', 'email' )
