DEBUG = True
ALLOWED_HOSTS = ['*', ]
DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'loanapp',
        'USER':'postgres',
        'PASSWORD':'$$@Access2018!',
        'TIMEZONE':'Africa/Nairobi',
    },
}   
#Loan Settings
BRAND_NAME = 'Jijenge Loans'
AUTO_APPROVE_CEILING = 5000
IPN_CONFIG ={
    'payouts_url':'https://ipn.quickbid.co.ke:7024/ipn/pay/',
    'app-key':'e2163f00d7e14f02a6d6b2479a74b8be',
    'app-secret':'10f73d4fdd3a4e25bcd838c465848f1e',
    'short_code' : '5802001',
}