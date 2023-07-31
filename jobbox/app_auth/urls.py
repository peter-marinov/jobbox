from django.urls import path

from jobbox.app_auth.views import LoginUserView,  RegisterUserView, LogoutUserView, profile_user, \
    update_profile, change_password, DeleteProfileView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/', profile_user, name='profile_user'),
    path('profile/edit/', update_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),

]
