from django.conf.urls.static import static
from django.conf import settings
from .views import *
from django.urls import path

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),  # dashboard
    path('tests/', all_tests, name='all_tests'),
    path('new-test/', new_test, name='new_test'),
    path('test-requests/', test_requests, name='test_requests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
