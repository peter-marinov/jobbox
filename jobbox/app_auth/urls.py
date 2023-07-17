from django.urls import path

from jobbox.app_auth.views import LoginUserView, RegisterUserView, RegisterHRView, LogoutUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('register/user/', RegisterUserView.as_view(), name='register_user'),
    path('register/hr/', RegisterHRView.as_view(), name='register_hr'),
    path('user/logout/', LogoutUserView.as_view(), name='logout_user'),

]
