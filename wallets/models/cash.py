from django.utils import timezone
from django.db import models, transaction
from django_enumfield import enum
from flex.ussd.utils.decorators import export
from factory.models import FactoryModel, QuerySet, Manager
from .base import BaseWallet, BaseTransaction


@export()
class Cash(BaseWallet):
    class Meta(BaseWallet.Meta):
        verbose_name = "loan wallet"
        verbose_name_plural = "loan wallets"

    def credit(self, amount, subject, **kw):
        with self.lock():
            del self.balance
            with transaction.atomic():
                obj = CashCredit.objects.create(
                    wallet=self,
                    amount=amount,
                    subject=subject,
                    initial_balance=self.balance,
                    **kw
                )
                self.balance = self.balance + amount
                self.save()
                return obj

    def debit(self, amount, subject, **kw):
        with self.lock():
            with transaction.atomic():
                if self.balance < amount:
                    raise ValueError("insufficient funds")

                del self.balance

                obj = CashDebit.objects.create(
                    wallet=self,
                    amount=amount,
                    subject=subject,
                    initial_balance=self.balance,
                    **kw
                )
                self.balance = self.balance - amount
                self.save()
                return obj


@export()
class CashTransaction(BaseTransaction):
    class Meta(BaseTransaction.Meta):
        verbose_name = "transaction"
        verbose_name_plural = "transactions"

    wallet = models.ForeignKey(Cash, models.CASCADE, related_name="transactions")


class CashCredit(CashTransaction):

    __type__ = BaseTransaction.Type.CREDIT

    class Meta(CashTransaction.Meta):
        proxy = True


class CashDebit(CashTransaction):

    __type__ = CashTransaction.Type.DEBIT

    class Meta(CashTransaction.Meta):
        proxy = True
