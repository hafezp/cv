from django.db 					import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers 					import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=11, unique=True)
	full_name = models.CharField(max_length=100, default='default')
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'  
	REQUIRED_FIELDS = ['full_name','phone_number'] 

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin 



class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'



class VerifyCodeModel(models.Model): 

	code = models.IntegerField()