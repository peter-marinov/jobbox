from django.urls import path

from jobbox.job.views import create_job, HrJobListView, description_job_view, EditJobView, \
    DeleteJobView, download_cv, DeleteCVView

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('my-hr-list/', HrJobListView.as_view(), name='my_hr_list'),
    # path('<int:pk>/', DescriptionJobView.as_view(), name='description_job'),
    path('<int:pk>/', description_job_view, name='description_job'),
    path('<int:pk>/edit', EditJobView.as_view(), name='edit_job'),
    path('<int:pk>/delete', DeleteJobView.as_view(), name='delete_job'),
    path('cv/<int:pk>/download/', download_cv, name='download_cv'),
    path('cv/<int:pk>/delete/', DeleteCVView.as_view(), name='delete_cv'),
    # path('create/', CreateJobView.as_view(), name='create_job'),
]