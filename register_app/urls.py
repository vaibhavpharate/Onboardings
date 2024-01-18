from django.urls import path
from .views import create_client,create_site,delete_site

urlpatterns = [
    path('create_client',create_client,name='create_client'),
    path('create_site',create_site,name='create_site'),
    path('delete_site/<str:site_id>',delete_site,name='delete_site')

]