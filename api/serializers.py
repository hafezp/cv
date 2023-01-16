
from django.contrib.auth    import get_user_model  
from rest_framework         import serializers
from cv.models              import Contact, Testimonial, IpAddress
from income.models          import Income, Category



# for superuser management
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id','full_name','email','phone_number','is_active', 'is_admin','is_superuser','last_login')

#for anon user self register
class AnonUserRegisterSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:							 
		model = get_user_model()
		fields = ('id','full_name','email', 'phone_number', 'password', 'password2')


		extra_kwargs = {                                
			'password': {'write_only':True},
		}

	def validate_email(self, value):
		if not value.endswith("@gmail.com" or "@yahoo.com"):
			raise serializers.ValidationError('we dont support fake mail !')
		return value
		
	def validate_full_name(self, value):
		if value == 'admin':
			raise serializers.ValidationError('full name cant be `admin`')
		return value

	def validate_password2(self, data):
		if not data['password2']:
			raise serializers.ValidationError('Enter password 2')
		if data['password'] != data['password2']:
			raise serializers.ValidationError('passwords dont match')
		return data


	def create(self, validated_data):
		del validated_data['password2']
		return get_user_model().objects.create_user(**validated_data) 


class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ('id','name', 'email', 'text')

class TestimonialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Testimonial
		fields = ('id','message', 'thumbnail', 'full_name', 'job_position')

class IpAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = IpAddress
		fields = ('id','ip_address', 'pub_date')

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id','title', 'slug', 'user')

class IncomeSerializer(serializers.ModelSerializer):

	
	def get_full_name(self, obj):		      				                                                      
		return f'{obj.user.full_name} - {obj.user.id}'    
	full_name = serializers.SerializerMethodField("get_full_name") 



	class Meta:
		model = Income
		fields = ('id','full_name', 'type', 'category','select','price','thumbnail', 'publish')







