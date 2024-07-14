from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE

# Create your models here.
class Transaction(models.Model):
    account=models.ForeignKey(UserBankAccount,related_name='transactions',on_delete=models.CASCADE)
    amount=models.DecimalField(decimal_places=2,max_digits=12)
    balance_after_transaction=models.DecimalField(decimal_places=2,max_digits=12)
    transaction_type=models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    loan_approve=models.BooleanField(default=False)
    bankrupt=models.BooleanField(default=False)
    class Meta:
        ordering=['timestamp']


from django.contrib.auth.models import User
# from django.db import models

# class UserBankAccount(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userbankaccount')
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     # other fields as necessary

#     def __str__(self):
#         return f'{self.user.username} - Balance: {self.balance}'
    



# class UserBankAccount(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userbankaccount')
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     account_number = models.CharField(max_length=20, unique=True)
#     # other fields as necessary

#     def __str__(self):
#         return f'{self.user.username} - Balance: {self.balance}'


