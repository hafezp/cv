from django.db 					import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators		import RegexValidator
from .managers 					import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(validators=[RegexValidator(
																regex=r'^09(1[0-9]|3[1-9]|2[1-9]|9[0-9])[0-9]{3}[0-9]{4}$',
																message="Phone number must be entered in the format: '09353967479"
												)],
									help_text="در فرمت 09353967479 وارد کنید",
									max_length=11,
									unique=True)
	username = models.CharField(max_length=15)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'  
	REQUIRED_FIELDS = ['username','phone_number'] 

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin 




# class OtpCode(models.Model):
# 	phone_number = models.CharField(max_length=11, unique=True)
# 	code = models.PositiveSmallIntegerField()
# 	created = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return f'{self.phone_number} - {self.code} - {self.created}'



# class VerifyCodeModel(models.Model): 

# 	code = models.IntegerField()