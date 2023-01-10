
from django.http        import Http404
from django.shortcuts   import get_object_or_404

from .models            import Income

class UserAccessMixin():
	
	def dispatch(self, request, pk,  *args, **kwargs):
		income = get_object_or_404(Income, pk=pk)
		if income.user == request.user or request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404('دسترسی غیرمجاز !')


class FieldsMixin():   
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			self.fields = '__all__'
		else:
			self.fields = ['id','type','category', 'select','price', 'thumbnail']     
		return super().dispatch(request, *args, **kwargs)


class FormFieldValidMixin():                           
	def form_valid(self, form):
		if self.request.user.is_superuser:
			form.save()
		else:
			self.obj = form.save(commit=False)
			self.obj.user = self.request.user	 

		return super().form_valid(form)


class SuperUserAccessMixin():
	def dispatch(self, request, pk,  *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404('permission denied !')


def persian_num_converter(mystr):
	numbers ={
		'0':'٠',
		'1':'١',
		'2':'٢',
		'3':'٣',
		'4':'٤',
		'5':'٥',
		'6':'٦',
		'7':'٧',
		'8':'٨',
		'9':'٩',
	}
	for e, p in numbers.items():

		mystr = mystr.replace(e, p)
	return mystr

class FormContextValidMixin():   
	'''persianazing type item of income model'''
					 
	def form_valid(self, form):

		self.obj = form.save(commit=False)
		
		self.obj.type = persian_num_converter(self.obj.type)
		self.obj.persianized_price = persian_num_converter(str(self.obj.persianized_price))


		return super().form_valid(form)




