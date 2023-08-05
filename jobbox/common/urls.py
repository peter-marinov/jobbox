from django.urls import path, include

from jobbox.common.views import index, AboutView, ContactUsList, EditContactUs, DeleteContactUs

urlpatterns = [
    path('', index, name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact-us/', include([
        path('', ContactUsList.as_view(), name='contact_us_list'),
        path('<int:pk>/edit', EditContactUs.as_view(), name='edit_contact_us'),
        path('<int:pk>/delete', DeleteContactUs.as_view(), name='delete_contact_us'),
    ])),
]
