from django.urls import path
from . import views

urlpatterns = [
    path('init', views.init, name='init'),
    path('create_file', views.create_file, name='create_file'),
    path('read_file', views.read_file, name='read_file'),
    path('write_file', views.write_file, name='write_file'),
    path('delete_file', views.delete_file, name='delete_file'),
    path('get_file_info', views.get_file_info, name='get_file_info'),
    path('copy_file', views.copy_file, name='copy_file'),
    path('read_dir', views.read_dir, name='read_dir'),
    path('create_dir', views.create_dir, name='create_dir'),
    path('delete_dir', views.delete_dir, name='delete_dir'),

    path('storage/heartbeat',
         views.storage_heartbeat, name='heartbeat'),
    path('storage/update_status',
         views.storage_update_status, name='update_status'),
]
