from django.urls import path

from jobbox.task.views import CreateHRTask, ListAllTasks, ListHRTask, EditHRTask, DeleteHRTask

urlpatterns = [
    path('', ListHRTask.as_view(), name='list_hr_task'),
    path('all/', ListAllTasks.as_view(), name='list_all_tasks'),
    path('create', CreateHRTask.as_view(), name='create_hr_task'),
    path('<int:pk>/edit', EditHRTask.as_view(), name='edit_hr_task'),
    path('<int:pk>/delete', DeleteHRTask.as_view(), name='delete_hr_task'),
]