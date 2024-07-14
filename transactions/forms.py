from django import forms
from .models import Transaction
from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 200000
        balance = account.balance
        amount = self.cleaned_data.get('amount')

        # Check if the bank is bankrupt
        if Transaction.objects.filter(bankrupt=True).exists():
            raise forms.ValidationError(
                'The bank is bankrupt. You cannot withdraw money at this time.'
            )

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You cannot withdraw more than your account balance'
            )

        return amount


class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount


from django import forms
from .models import UserBankAccount

class TransferForm(forms.Form):
    recipient_account_number = forms.IntegerField()
    amount = forms.DecimalField(max_digits=12, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.user_account = kwargs.pop('user_account', None)
        super().__init__(*args, **kwargs)

    def clean_recipient_account_number(self):
        account_number = self.cleaned_data.get('recipient_account_number')
        try:
            recipient_account = UserBankAccount.objects.get(account_no=account_number)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError('Account number does not exist.')
        return recipient_account

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        if self.user_account and self.user_account.balance < amount:
            raise forms.ValidationError('Insufficient balance.')
        return cleaned_data

