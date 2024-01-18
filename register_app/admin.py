from django.contrib import admin
from .models import  Clients,Site_Configs,SiteVerification

# from django.contrib.auth import get_user_model

# Register your models here.
# admin.site.register(get_user_model())

# admin.site.register(Clients)
admin.site.register(Clients)
admin.site.register(Site_Configs)
admin.site.register(SiteVerification)
