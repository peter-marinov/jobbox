from django.urls import path

from jobbox.app_auth.views import LoginUserView,  RegisterUserView, LogoutUserView, profile_user, \
    update_profile, change_password, DeleteProfileView, AllProfiles, EditProfileAdministrator, \
    DeleteProfileAdministrator, ChangeEmailAndRightsAdministrator

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/', profile_user, name='profile_user'),
    path('profile/edit/', update_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),
    path('all/', AllProfiles.as_view(), name='all_profiles'),
    path('<int:pk>/edit', EditProfileAdministrator.as_view(), name='edit_profile_administrator'),
    path('<int:pk>/delete', DeleteProfileAdministrator.as_view(), name='delete_profile_administrator'),
    path('<int:pk>/change', ChangeEmailAndRightsAdministrator.as_view(), name='change_user_administrator'),


]
