from django.urls    import path
from .views         import ContactFormView, PostDetailView

app_name = 'cv'

urlpatterns = [ 
# path('single/<int:id>', PostDetailView.as_view(), name = 'post_detail'),
path('', ContactFormView.as_view(), name='index'),

]