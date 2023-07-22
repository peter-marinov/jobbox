from django.urls import path

from jobbox.common.views import index, AboutView

urlpatterns = [
    path('', index, name='index'),
    path('about/', AboutView.as_view(), name='about'),

]
