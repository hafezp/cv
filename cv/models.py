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


    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = 'زمان ارسال'

    def get_absolute_url(self):
        return reverse('cv:index')

    def __str__(self):
        return '{}'.format(self.name)








