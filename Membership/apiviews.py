from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer
import json
from rest_framework import generics


class CustomerList(APIView):
	def get(self, request):
		customers = Member.objects.all()
		data = MemberSerializer(customers, many=True).data
		return Response(json.dumps(data))

class customersearch(generics.ListAPIView):

	serializer_class =MemberSerializer
	def get_queryset(self):
		queryset=Member.object.all()
		first_name = self.request.query_params.get('fname', None)
		if first_name is not None:
			queryset = queryset.filter(Member__first_name=first_name)
		return queryset