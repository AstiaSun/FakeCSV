"""Schema url config."""

from django.urls import path

from schema import views

app_name = 'schema'

urlpatterns = [
    path('list', views.schema_list, name='schema_list'),
    path('create', views.schema_create, name='schema_create'),
    path('<str:pk>/generate', views.generate_csv_from_schema, name='generate'),
    path('files/<str:pk>', views.download_csv_file, name='download_csv_file')
]
