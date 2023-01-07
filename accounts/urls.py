
from django.urls import path

from .views import activate

from .views import (Login,
                    Logout,
                    ProfileView,
                    PasswordChange,
                    PasswordReset,
                    PasswordResetConfirm,
                    UserRegisterVerifyCodeView,
                    )

from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView)

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
]

urlpatterns += [
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_code'),

    
  ]

