from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Recipient)
admin.site.register(models.RecipientOneMany)
admin.site.register(models.RecipientMany)