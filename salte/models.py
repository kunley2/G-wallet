from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext_lazy as _




# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2)
    account_name = models.CharField(_("account name"), max_length=250)
    account_number = models.CharField(_("account number"), max_length=100)
    phone_number = models.CharField(_("phone number"), max_length=15)
    date_of_birth = models.DateField('date of birth')
    # passcode = models.IntegerField('pass_code',max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='images')



class Trnansaction(models.Model):
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




