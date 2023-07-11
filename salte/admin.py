from django.contrib import admin
from .models import Account, Transaction

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','created_at','photo',"image_tag","updated_at")

admin.site.register(Account,AccountAdmin)