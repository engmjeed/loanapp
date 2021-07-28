from django_enumfield import enum


class WalletType(enum.Enum):
    
    CASH = 1
    


class TransactionType(enum.Enum):
    CREDIT = 1
    DEBIT = 2
