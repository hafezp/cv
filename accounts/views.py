

from django.contrib.auth.views 						import (PasswordChangeView,
															PasswordResetView,
															PasswordResetConfirmView)

from django.contrib.auth.mixins 					import LoginRequiredMixin
from django.contrib.auth.views 						import LoginView, LogoutView
from django.views.generic 							import UpdateView
from django.urls 									import reverse_lazy
from django.http 									import HttpResponse
from django.shortcuts 								import render, redirect
from django.contrib.sites.shortcuts 				import get_current_site
from django.utils.encoding 							import force_bytes, force_str
from django.utils.http 								import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader 						import render_to_string
from django.core.mail 								import EmailMessage
from django.views 									import View
import random

from .forms 										import ProfileForm, VerifyCodeForm, UserRegistrationForm
from .tokens 										import account_activation_token
from .models 										import User, OtpCode
from .mixins										import AccessLimitMixin




def UserRegisterView(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('registration/acc_active_email.html', {  
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
			email.send()
			return HttpResponse('یک ایمیل برای شماارسال کردیم، لطفاایمیل خودرا تایید کنید تا بتوانید از امکانات سایت استفاده کنید')
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/signup.html' , {'form': form}) 


def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		return HttpResponse(' باسپاس از شما اکانت شما فعال شد http://localhost:8000/account/login/ ')

	else:
		return HttpResponse('Activation link is invalid!')


class Login(AccessLimitMixin, LoginView):
	pass


class Logout(LogoutView):
	pass


class ProfileView(LoginRequiredMixin, UpdateView):
	model = User
	template_name = "registration/profile.html"
	form_class = ProfileForm
	success_url = reverse_lazy('account:profile')
		
	def get_object(self):
		return User.objects.get(pk=self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super(ProfileView, self).get_form_kwargs()
		kwargs.update({
			'user':self.request.user
			})
		return kwargs


class PasswordChange(PasswordChangeView):
	success_url = reverse_lazy('account:password_change_done')




class PasswordReset(PasswordResetView):
	success_url = reverse_lazy('account:password_reset_done')


	

class PasswordResetConfirm(PasswordResetConfirmView):
	success_url = reverse_lazy('account:password_reset_complete')



class UserRegisterVerifyCodeView(LoginRequiredMixin, View):
	"""
	need to optimize by setup() method
	"""
	form_class = VerifyCodeForm

	def get(self, request):

		form = self.form_class
		random_code = random.randint(1000, 9999)
		otp = OtpCode.objects.filter(phone_number=self.request.user.phone_number).exists()
		user_condition = self.request.user.is_admin

		if not otp and not user_condition:
			OtpCode.objects.create(phone_number=self.request.user.phone_number, code=random_code)
		
		return render(request, 'registration/verify.html', {'form':form,'admin':self.request.user.is_admin})


	def post(self, request):

		code_instance = OtpCode.objects.get(phone_number=self.request.user.phone_number)
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['code'] == code_instance.code:
	
				user = self.request.user
				user.is_admin = True
				user.save()

				code_instance.delete()

				return redirect('/admin')
			else:

				return redirect('account:verify_code')
		return redirect('income:home')


