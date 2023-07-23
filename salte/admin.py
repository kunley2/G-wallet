from django.contrib import admin
from .models import Account, Transaction

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','account_number','passcode','created_at','photo',"image_tag","updated_at",'account_name')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type','amount')
    
admin.site.register(Account,AccountAdmin)