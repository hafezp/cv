from django.contrib.auth    import get_user_model  

from rest_framework         import serializers
from cv.models              import Contact, Testimonial, IpAddress

from income.models          import Income, Category




# for superuser management
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id','username','email','phone_number','is_active', 'is_admin','is_superuser','last_login','password')

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id','username','email','phone_number','password')

		extra_kwargs = {                                
			'password': {'write_only':True},
		}

	def validate_email(self, value):
		if not value.endswith("@gmail.com" or "@yahoo.com" or ".ir"):
			raise serializers.ValidationError('we dont support fake mail and just support Gmail and Yahoo!')
		return value

#for anon user self register
class AnonUserRegisterSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:							 
		model = get_user_model()
		fields = ('username','email', 'phone_number', 'password', 'password2')

		extra_kwargs = {                                
			'password': {'write_only':True},
		}

	def validate_email(self, value):
		if not value.endswith("@gmail.com" or "@yahoo.com" or ".ir"):
			raise serializers.ValidationError('we dont support fake mail !')
		return value
		
	def validate_username(self, value):
		if value == 'admin':
			raise serializers.ValidationError('full name cant be `admin`')
		return value

	def validate(self, data):
		if data['password'] != data['password2']:
			raise serializers.ValidationError('passwords dont match')
		return data


	def create(self, validated_data):
		del validated_data['password2']
		return get_user_model().objects.create_user(**validated_data)


class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = ('name', 'email', 'text')

class TestimonialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Testimonial
		fields = ('message', 'thumbnail', 'full_name', 'job_position')
		

class IpAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = IpAddress
		fields = ('id','ip_address', 'pub_date')


class UserForCategorySerializer(serializers.ModelSerializer):

	class Meta:							 
		model = get_user_model()
		fields = ('username',)

class CategorySerializer(serializers.ModelSerializer):

	"""The First Category Model serialiser by default"""

	user = UserForCategorySerializer(many=True, read_only=True)
	
	class Meta:
		model = Category
		fields = ('id','title', 'slug', 'user')

class CategoryCreateSerializer(serializers.ModelSerializer):

	"""The Second Category Model serialiser for create"""

	def create(self, validated_data):
		"""Autocomplete of User"""
		new_category = Category(
			title=validated_data['title'],
			slug=validated_data['slug'],
			)	
		new_category.save()
		new_category.user.add(self.context['request'].user)
		return new_category

	
	class Meta:
		model = Category
		fields = ('title', 'slug')

		
class IncomeSerializer(serializers.ModelSerializer):

	"""The First Income Model serialiser by default"""

	category = CategorySerializer(many=True, read_only=True)

	def get_user(self, obj):	

		return f'{obj.user.username} - {obj.user.id}'    

	user = serializers.SerializerMethodField("get_user") 

	class Meta:
		model = Income
		fields = ('id','user', 'explanation', 'category','select','price','thumbnail', 'publish')

class IncomeCreateSerializer(serializers.ModelSerializer):

	"""The Second Income Model serialiser for create"""



	def create(self, validated_data):
		new_income = Income(
			explanation=validated_data['explanation'],
			select=validated_data['select'],
			price=validated_data['price'],
			)
		new_income.user = self.context['request'].user	
		new_income.save()
		new_income.category.set(validated_data['category'])
		return new_income


	class Meta:
		model = Income
		fields = ('explanation', 'category','select','price','thumbnail', 'publish')




