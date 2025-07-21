from django.contrib import admin
from .models import CustomUser , Project , Reclamation , Logs , Client

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Reclamation)
admin.site.register(Logs)
admin.site.register(Client)