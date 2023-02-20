from django.db          import models
from django.utils       import timezone
from django.utils.html  import format_html
from django.urls        import reverse

from extensions.utils   import jalali_converter
# Create your models here.




class TimeStamped(models.Model):

	publish = models.DateTimeField(default=timezone.now)
	created = models.DateField(auto_now_add=True, null=True, blank=True)
	updated = models.DateField(auto_now=True, null=True)

	class Meta:
		abstract = True


class Testimonial(TimeStamped):

	message = models.TextField(max_length=280, verbose_name='پیام')
	thumbnail = models.ImageField(upload_to='media/', null=True, blank=True) 
	full_name = models.CharField(max_length=30)
	job_position = models.CharField(max_length=30)

	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = 'زمان انتشار'

		
	def thumbnail_tag(self):
		if self.thumbnail:
			return format_html("<img width=80 src='{}' >".format(self.thumbnail.url))
		else:
			return ""
	thumbnail_tag.short_description = 'تصویر'


	def get_absolute_url(self):
		return reverse('cv:index')


	def __str__(self):
		return '{}'.format(self.full_name)


class Post(TimeStamped):

	title = models.CharField(max_length=200, verbose_name="عنوان")
	text = models.TextField(max_length=1000)
	thumbnail = models.ImageField(upload_to='media/', null=True, blank=True) 

	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = 'زمان انتشار'

	def thumbnail_tag(self):
		if self.thumbnail:
			return format_html("<img width=80 src='{}' >".format(self.thumbnail.url))
		else:
			return ""
	thumbnail_tag.short_description = 'تصویر'

	def get_absolute_url(self):
		return reverse('cv:index')

	def __str__(self):
		return '{}'.format(self.title)


class Contact(TimeStamped):

	name = models.CharField(max_length=25, verbose_name="Name")
	email = models.EmailField(verbose_name='Email')
	text = models.TextField(max_length=250, verbose_name='Message')

	class Meta:
		verbose_name = "پیام"
		verbose_name_plural = "پیام ها"
		ordering = ['-publish']


	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = 'زمان ارسال'

	def get_absolute_url(self):
		return reverse('cv:index')

	def __str__(self):
		return '{}'.format(self.name)


class IpAddress(models.Model):
	pub_date = models.DateTimeField('زمان اولین بازدید', default=timezone.now)
	ip_address = models.GenericIPAddressField(blank=True, null=True ,verbose_name='آدرس')

	def first_time_view(self):
		return jalali_converter(self.pub_date)
	first_time_view.short_description = 'زمان اولین بازدید'

	class Meta:
		verbose_name = "آی‌پی"
		verbose_name_plural = "آی‌پی ها"
		ordering = ['-pub_date']

	def __str__(self):
		return self.ip_address






