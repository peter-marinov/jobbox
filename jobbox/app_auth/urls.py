from django.urls import path

from jobbox.app_auth.views import LoginUserView, RegisterUserView, RegisterHRView, LogoutUserView, profile_user, \
    update_profile, DeleteProfileView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('register/user/', RegisterUserView.as_view(), name='register_user'),
    path('register/hr/', RegisterHRView.as_view(), name='register_hr'),
    path('user/logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/', profile_user, name='profile_user'),
    # path('profile/<int:pk>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/edit/', update_profile, name='edit_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),

]
