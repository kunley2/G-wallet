from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe




# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2, default=0)
    account_name = models.CharField(_("account name"), max_length=250)
    account_number = models.CharField(_("account number"), max_length=100,unique=True)
    phone_number = models.CharField(_("phone number"), max_length=15,unique=True)
    date_of_birth = models.DateField('date of birth')
    passcode = models.IntegerField('pass_code',max_length=6)
    photo = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self): # new
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

    class Meta:
        db_table = 'Account'
        managed = True



class Transaction(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SUCCESS = 'success', _('Success')
        FAIL = 'fail', _('Fail')

    class TransactionType(models.TextChoices):
        BANK_TRANSFER_FUNDING = 'funding', _('Bank Transfer Funding')
        BANK_TRANSFER_PAYOUT = 'payout', _('Bank Transfer Payout')
        DEBIT_USER_WALLET = 'debit user wallet', _('Debit User Wallet')
        CREDIT_USER_WALLET = 'credit user wallet', _('Credit User Wallet')

    account = models.ForeignKey(Account,on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=100, choices=TransactionType.choices)
    amount = models.DecimalField(_("amount"), max_digits=100, decimal_places=2)
    status = models.CharField(max_length=100,choices=STATUS.choices,default=STATUS.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Transaction'
        managed = True




