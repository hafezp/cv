from rest_framework import routers
from django.urls    import path
from .views         import (
                            ContactListCreateView,
                            ContractRetrieveUpdateDestroyView,
                            UserListView,
                            UserCreateView,
                            UserUpdateView,
                            UserDeleteView,
                            UserProfileViewSet,
                            AnonUserRegisterView,
                            IncomeViewSet,
                            TestimonialViewSet,
                            IPAddressListView,
                            CategoryViewSet

                            )

app_name = 'api'

urlpatterns = [ 
path("contact/list-create", ContactListCreateView.as_view(), name="contact-list-create"),
path("contact/retrieve-update-destroy/<int:pk>", ContractRetrieveUpdateDestroyView.as_view(), name="contract-retrieve-update-destroy"),

path("user/list", UserListView.as_view(), name="user-list"),
path("user/create", UserCreateView.as_view(), name="user-create"),
path("user/update/<int:id>", UserUpdateView.as_view(), name="user-update"),
path("user/del/<int:id>", UserDeleteView.as_view(), name="user-delete"),

path("ip", IPAddressListView.as_view(), name="ip-list"),

path("register", AnonUserRegisterView.as_view(), name="register"),

]


router = routers.SimpleRouter()
router.register('profile', UserProfileViewSet, basename='profile')
router.register('income', IncomeViewSet, basename='income')
router.register('category', CategoryViewSet, basename='category')
router.register('testimonial', TestimonialViewSet, basename='testimonial')
urlpatterns += router.urls
