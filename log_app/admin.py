from django.contrib import admin
from .models import Youtility_logs,Mobileservices_logs,Error_logs,Reports_logs
# Register your models here.

admin.site.register(Youtility_logs)
admin.site.register(Error_logs)
admin.site.register(Mobileservices_logs)
admin.site.register(Reports_logs)