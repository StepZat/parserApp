from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.about, name='about'),
    path('about/', views.about, name='about'),
    path('uploaddicts/', views.uploadDicts, name='uploaddicts'),
    path('query/', views.query, name='query'),
    path('result/', views.load_vacancies, name='load_jobs'),
    path('export/windows', views.export_to_csv_windows, name='export_to_csv_win'),
    path('export/unix', views.export_to_csv_unix, name='export_to_csv_unix')
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
