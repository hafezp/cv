
from .models 						import User
from django 						import forms
from django.core 					import validators
from django.core.exceptions 		import ValidationError
from django.contrib.auth.forms 		import ReadOnlyPasswordHashField





class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user') 
		super(ProfileForm, self).__init__(*args, **kwargs)
		if not user.is_superuser:
			self.fields['phone_number'].disabled = True
			self.fields['email'].disabled = True

	class Meta:
		model = User
		fields = ['email','phone_number','full_name']


# for django admin 
class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('passwords dont match')
		return cd['password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

# for django admin 
class UserChangeForm(forms.ModelForm):  
	password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


#anon user self-register
class UserRegistrationForm(forms.Form):

	email = forms.EmailField(widget=forms.EmailInput,
							 validators=[validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')],
							 label='ایمیل')

	full_name = forms.CharField(widget=forms.TextInput,
								label='نام کامل')

	phone = forms.CharField(max_length=11, 
							validators=[validators.MinLengthValidator(10, 'تعداد کاراکترهای شماره همراه وارد شده نمیتواند کمتر از 10 باشد')],
							label='شماره موبایل')

	password1 = forms.CharField(
		widget=forms.PasswordInput,
		label='کلمه ی عبور'
	)

	password2 = forms.CharField(
		widget=forms.PasswordInput,
		label='تکرار کلمه ی عبور'
	)

	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists')

		if not email.endswith("@gmail.com" or "@yahoo.com"):
			raise ValidationError("Sorry, perhaps you use fakemail but now we just accept Gmail and Yahoo services ")

		return email


	def clean_phone(self):
		phone = self.cleaned_data['phone']
		user = User.objects.filter(phone_number=phone).exists()
		if user:
			raise ValidationError('This phone number already exists')
		return phone


	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('کلمه های عبور مغایرت دارند')
		return cd['password2']


	def save(self, commit=True):

		cd = self.cleaned_data
		user = User(email=cd['email'], full_name=cd['full_name'],
		 			phone_number=cd['phone'])
		user.set_password(cd['password2'])
		return user


# class VerifyCodeForm(forms.ModelForm):

# 	class Meta:
# 		model = VerifyCodeModel
# 		fields = '__all__'            



