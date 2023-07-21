from django.urls import path

from jobbox.job.views import create_job, HrJobListView, DescriptionJobView, EditJobView, DeleteJobView

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('my-hr-list/', HrJobListView.as_view(), name='my_hr_list'),
    path('<int:pk>/', DescriptionJobView.as_view(), name='description_job'),
    path('<int:pk>/edit', EditJobView.as_view(), name='edit_job'),
    path('<int:pk>/delete', DeleteJobView.as_view(), name='delete_job')
    # path('create/', CreateJobView.as_view(), name='create_job'),
]