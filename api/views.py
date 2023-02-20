from rest_framework.generics 	import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views       import APIView
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.viewsets	import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.shortcuts 			import get_object_or_404
from django.contrib.auth    	import get_user_model  

from cv.models 					import Contact, Testimonial, IpAddress
from income.models              import Income, Category

from .permissions				import IsSuperUser,IsOwnerOrReadOnly

from .serializers 				import (ContactSerializer, 
										UserSerializer,
										AnonUserRegisterSerializer,
										IncomeSerializer,
										IncomeCreateSerializer,
										TestimonialSerializer,
										IpAddressSerializer,
										CategorySerializer,
										CategoryCreateSerializer,
										UserProfileSerializer)




class ContactListCreateView(ListCreateAPIView):
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer

class ContractRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):    
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer


class IncomeViewSet(ModelViewSet):

	queryset = Income.objects.all()
	# serializer_class = IncomeSerializer

	serializer_classes = {
		'create': IncomeCreateSerializer, # serializer used on post
	}

	default_serializer_class = IncomeSerializer # Your default serializer

	def get_serializer_class(self): # for Viewset
		return self.serializer_classes.get(self.action, self.default_serializer_class)


	def get_permissions(self):  		
		if self.action in ['list']:
			permission_classes = [IsSuperUser]
		else:
			permission_classes = [IsOwnerOrReadOnly]

		return [permission() for permission in permission_classes ]


class CategoryViewSet(ModelViewSet):

	queryset = Category.objects.all()
	# serializer_class = CategorySerializer

	serializer_classes = {
		'create': CategoryCreateSerializer, # serializer used on post
	}

	default_serializer_class = CategorySerializer # Your default serializer

	def get_serializer_class(self): # for Viewset
		return self.serializer_classes.get(self.action, self.default_serializer_class)


	def get_permissions(self):  		
		if self.action in ['list']:
			permission_classes = [IsSuperUser]
		else:
			permission_classes = [IsOwnerOrReadOnly]

		return [permission() for permission in permission_classes ]


class TestimonialViewSet(ModelViewSet):

	queryset = Testimonial.objects.all()
	serializer_class = TestimonialSerializer


class IPAddressListView(APIView):

	permission_classes = [IsSuperUser]

	def get(self, request):
		ips = IpAddress.objects.all()
		ser_data = IpAddressSerializer(instance=ips, many=True) 
		return Response(data=ser_data.data, status=status.HTTP_200_OK)      


# manage users by supersuer
class UserListView(APIView):

	permission_classes = [IsSuperUser]
	throttle_scope = 'users'

	def get(self, request):
		users = get_user_model().objects.all()
		srz_data = UserSerializer(instance=users, many=True).data
		return Response(srz_data, status=status.HTTP_200_OK)

class UserCreateView(APIView):
	"""
		Create a new user
	"""
	permission_classes = [IsSuperUser,]
	serializer_class = AnonUserRegisterSerializer
 
	def post(self, request):
		srz_data = AnonUserRegisterSerializer(data=request.data)
		if srz_data.is_valid():
			# srz_data.save()
			srz_data.create(srz_data.validated_data)
			return Response(srz_data.data, status=status.HTTP_201_CREATED)
		return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
	permission_classes = [IsSuperUser,]

	def put(self, request, id):
		user = get_object_or_404(get_user_model().objects.all(), id=id)
		srz_data = UserSerializer(instance=user, data=request.data, partial=True)
		if srz_data.is_valid():
			srz_data.save()
			return Response(srz_data.data, status=status.HTTP_200_OK)
		return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
	permission_classes = [IsSuperUser,]

	def delete(self, request, id):
		user = get_object_or_404(get_user_model().objects.all(), id=id)
		user.delete()
		return Response({'message': 'user deleted'}, status=status.HTTP_200_OK)

# anon user register
class AnonUserRegisterView(APIView):

	def post(self, request):
		ser_data = AnonUserRegisterSerializer(data=request.data)
		if ser_data.is_valid(): 
			ser_data.create(ser_data.validated_data)
			return Response(ser_data.data, status=status.HTTP_201_CREATED)
		return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

# anon user profile
class UserProfileViewSet(ViewSet):

	permission_classes = [IsAuthenticated,]
	queryset = get_user_model().objects.all() 
	permission_context = {'permission denied': 'permission denied'}


	def get_permissions(self):
		return super().get_permissions()


	def retrieve(self, request, pk=None):
		user = get_object_or_404(self.queryset, pk=pk)
		if user != request.user:  
			return Response(self.permission_context)
		srz_data = UserProfileSerializer(instance=user)
		return Response(data=srz_data.data)

	def partial_update(self, request, pk=None):
		user = get_object_or_404(self.queryset, pk=pk)
		if user != request.user:  
			return Response(self.permission_context)
		srz_data = UserProfileSerializer(instance=user, data=request.POST, partial=True)
		if srz_data.is_valid():
			srz_data.save()
			return Response(data=srz_data.data)
		return Response(data=srz_data.errors)

	def destroy(self, request, pk=None):
		user = get_object_or_404(self.queryset, pk=pk)
		if user != request.user:
			return Response(self.permission_context)
		user.is_active = False
		user.save()
		return Response({'message':'user deactivated'})