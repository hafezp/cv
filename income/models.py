from django.db.models.deletion 	import SET_NULL
from django.db 					import models
from django.core.exceptions 	import ValidationError
from django.urls 				import reverse
from django.utils 				import timezone
from django.utils.html 			import format_html
from django.db.models 			import Q

from extensions.utils 			import jalali_converter, persian_num_converter
from accounts.models 			import User
# Create your models here.

class TimeStampedModel(models.Model):

	publish = models.DateTimeField(default=timezone.now)
	created = models.DateField(auto_now_add=True, null=True, blank=True)
	updated = models.DateField(auto_now=True, null=True)

	class Meta:
		abstract = True


class Category(models.Model):

	title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
	slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی")
	user = models.ManyToManyField(User, blank=True, related_name='category', verbose_name='کاربر')
	class Meta:
		verbose_name_plural = "دسته بندی ها"

	def get_absolute_url(self):
		return reverse('income:list')

	def __str__(self):
		return self.title


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(" حداکثر سایز فاکتور %sMB میباشد" % str(megabyte_limit))
		
class Income(TimeStampedModel):

	INCOME_CHOICES = (
		('in', 'دخل'),
		('out', 'خرج'),
		)
	user = models.ForeignKey(User, on_delete=SET_NULL,null=True,blank=True)
	type = models.CharField(max_length=50, verbose_name='توضیح هزینه')
	category = models.ManyToManyField(Category, related_name='income', verbose_name='دسته بندی')
	select = models.CharField(max_length=3, choices=INCOME_CHOICES, default='دخل', verbose_name='نوع هزینه')
	price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="درآمد")
	thumbnail = models.ImageField(upload_to='media/',validators=[validate_image] ,null=True, blank=True, help_text="حداکثر حجم 1 مگابایت می باشد.") 


	# objects = IncomeSearchManager()



	def get_absolute_url(self):
		return reverse('income:incomelist')
	
	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = 'زمان انتشار'

	def persianized_price(self):
		return persian_num_converter(str(self.price))
	persianized_price.short_description = 'مبلغ'
		
	def thumbnail_tag(self):
		if self.thumbnail:
			return format_html("<img width=80 src='{}' >".format(self.thumbnail.url)) 
		else:
			return "no image"
	thumbnail_tag.short_description = 'فاکتور'


	def __str__(self):
		return '{}'.format(self.type)

