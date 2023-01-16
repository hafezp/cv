from django.urls    import path
from .views         import ContactFormView

app_name = 'cv'

urlpatterns = [ 

path('', ContactFormView.as_view(), name='index'),

]