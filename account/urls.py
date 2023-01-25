from django.urls import path, re_path
from .views import RegistrationView, LoginView, ActivationView, \
    LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView, \
    register_by_access_token, authentication_test

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view()),
    # logining via google
    re_path('register-by-access-token/' + \
            r'social/(?P<backend>[^/]+)/$', register_by_access_token),
    path('login-via-google/', authentication_test),
]
