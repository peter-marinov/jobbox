from django.urls import path

from jobbox.common.views import index

urlpatterns = [
    path('', index, name='index')
]
