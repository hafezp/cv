
from django.contrib import admin  

from .models        import Testimonial, Post, Contact
# Register your models here.

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = ('full_name','jpublish','thumbnail_tag','job_position')
    list_filter = ('full_name',)                  
    search_fields = ('full_name', 'job_position')			

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title','text','thumbnail_tag','jpublish')
    list_filter = ('title',)                  
    search_fields = ('title', 'text')			

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ('name','email','text','jpublish')
    list_filter = ('email',)                  
    search_fields = ('email', 'text')			


