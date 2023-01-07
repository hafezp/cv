
from django 					import forms
from django.core.exceptions 	import ValidationError

from .models 					import Contact

class ContactForm(forms.ModelForm):

	class Meta:
		
		model = Contact
		fields = ('name','email','text')
		
		widgets = {
			'text': forms.Textarea(attrs={'rows':5, 'cols':40})
		}

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if not email.endswith("@gmail.com" or "@yahoo.com"):
			raise ValidationError()

		return email

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			
			self.fields[field].widget.attrs.update({

		  'class': 'form-control',
		  'required': True,
		
		})


