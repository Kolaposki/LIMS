from django.conf.urls.static import static
from django.conf import settings
from .views import *
from django.urls import path

urlpatterns = [
    path('', dashboard, name='dashboard'),  # dashboard
    path('dashboard/', dashboard, name='dashboard'),  # dashboard
    path('settings/', user_settings, name='user_settings'),

    path('tests/', all_tests, name='all_tests'),
    path('test/<str:test_uuid>/', test_details, name="test_details"),
    path('new-test/', new_test, name='new_test'),
    path('test-requests/', test_requests, name='test_requests'),

    path('laboratories/', laboratories, name='laboratories'),
    path('laboratory/<str:department>', lab_tests, name='lab_tests'),

    path('samples/', all_samples, name='all_samples'),
    path('new-sample/', new_sample, name='new_sample'),
    path('samples/<str:sample_type>', sample_list, name='sample_list'),

    path('reports/', all_reports, name='all_reports'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
