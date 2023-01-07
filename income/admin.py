
from django.contrib 				import admin
from .models 						import Income, Category


# Register your models here.


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
	list_display = ('id','user','type','display_category','select','persianized_price','jpublish','thumbnail_tag')
	list_filter = ('user', 'type')                  
	search_fields = ('title', 'status')			
	ordering = ['user', 'type']		

	def display_category(self,obj):                   
		return ', '.join([ category.title for category in obj.category.all() ])
	display_category.short_description = 'دسته بندی'		




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id','title','display_user','slug')

	prepopulated_fields = {'slug':('title',)} 

	def display_user(self,obj):                   
		return ', '.join([ user.full_name for user in obj.user.all() ])
	display_user.short_description = 'کاربر'		


