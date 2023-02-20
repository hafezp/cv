
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins 	import LoginRequiredMixin
from django.views.generic 			import ListView, DetailView, CreateView, UpdateView
from django.shortcuts 				import get_object_or_404, redirect, render
from django.utils.text 				import slugify
from django.urls 					import reverse, reverse_lazy
from django.views.generic.edit 		import DeleteView
from django.db.models 				import Count ,Q, Sum
from datetime 						import datetime, timedelta
from django.views                   import View

from .mixins 						import FormFieldValidMixin, FieldsMixin, UserAccessMixin, FormContextValidMixin
from .models 						import Income, Category
from .forms							import CategoryCreateForm

import random


 
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


@login_required
def home(request):

	all_incomes = Income.objects.all()
	sum_earning = all_incomes.filter(user=request.user, select='in').aggregate(sum_earning=Sum('price'))
	sum_spending = all_incomes.filter(user=request.user, select='out').aggregate(sum_spending=Sum('price'))

	# convert values to str
	v1 = ''.join(map(str, sum_earning.values()))
	v2 = ''.join(map(str, sum_spending.values()))

	# convert values to persian numbers
	new_v1 = persian_num_converter(v1)
	new_v2 = persian_num_converter(v2)

	
	if new_v1 != 'None' and new_v2 != 'None':
		diff = int(new_v1) - int(new_v2)
		new_diff = persian_num_converter(str(diff))

	elif new_v1 == 'None' and new_v2 != 'None':
		new_v1 = ''
		diff =  - int(new_v2)
		new_diff = persian_num_converter(str(diff))

	elif new_v2 == 'None' and new_v1 != 'None':
		new_v2 = ''
		diff = int(new_v1) 
		new_diff = persian_num_converter(str(diff))

	elif new_v1 == 'None' and new_v2 == 'None':
		new_v1 = ''
		new_v2 = ''
		new_diff =''

	context = {

	'new_v1': new_v1,
	'new_v2': new_v2,
	'new_diff': new_diff,

	}
	return render(request, 'income/home.html', context)


class IncomeList(LoginRequiredMixin, View):
	

	def setup(self, request, *args, **kwargs):
		self.income = Income.objects.all()
		return super().setup(request, *args, **kwargs)

	def get(self, request):
		categories = Category.objects.all()

		# last_month = datetime.today() - timedelta(days=30)
		if self.request.user.is_superuser:
			# income =  Income.objects.all().annotate(count=Count('hits', filter=Q(incomehit__created__gt=last_month))).order_by('-count', '-publish')
			income =  self.income
			return render(request, 'income/income_list.html', {'income':income, 'category':categories}) 
		else:
			income = self.income.filter(user=self.request.user)
			return render(request, 'income/income_list.html', {'income':income, 'category':categories})
	

class IncomeCreate(LoginRequiredMixin, FormFieldValidMixin, FieldsMixin, FormContextValidMixin, CreateView):
	model = Income
	template_name = "income/income-create-update.html"


class IncomeUpdate(UserAccessMixin, FormFieldValidMixin, FieldsMixin, FormContextValidMixin, UpdateView):
	model = Income
	template_name = "income/income-create-update.html"


class IncomeDelete(UserAccessMixin, DeleteView):
	model = Income
	success_url = reverse_lazy('income:incomelist')


class IncomeDetail(LoginRequiredMixin, DetailView):
	model = Income
	def get_object(self):
		id=self.kwargs.get('id')
		income =  get_object_or_404(Income.objects.all(), id=id)
		return income


class CategoryCreateView(LoginRequiredMixin, View):
	form_class = CategoryCreateForm

	def get(self, request, *args, **kwargs):
		form = self.form_class
		return render(request, 'income/category_create.html', {'form':form})


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_category = form.save(commit=False)
			# new_category.slug = slugify(form.cleaned_data['title'][:30])
			new_category.slug = slugify(str(random.randint(100, 999)))
			new_category.save()
			new_category.user.add(request.user)

			return redirect('income:create')


class SearchIncomeView(LoginRequiredMixin, ListView):
	template_name = 'income/search_list.html'
	paginate_by = 2
	context_object_name = 'income'
	
	def get_queryset(self):
		query = self.request.GET.get('q')
		if query is not None:
			lookup = Q(explanation__icontains=query) | Q(category__title__icontains=query)
			return Income.objects.filter(lookup).distinct()
		return Income.objects.all()


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.request.GET.get('q')
		return context


