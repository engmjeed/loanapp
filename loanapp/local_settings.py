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
    'short_code' : '5802002',
}
VARIABLES={'CONSUMER_KEY':'Q0bGiI76wVBhN7VDIuZaJAtEiTitNPic',
		   'CONSUMER_SECRET':'AP2T22ihN4AWUCQO',
		   'BUSINESS_SHORTCODE':'5802002',
           'Timestamp':'20210724132847',
		   'DEFAULTCALLBACKURL':'https://loans.jijenge.co.ke:6060/ipn/checkout-response/',
		   'PASSWORD':'NTgwMjAwMjgyODg3NmU4ZGM3MTMzYmIxNTY4MjBhNDMzN2Q3ZWYwYWI1ZmQ3MzI5MzgwNThiMzM1Yzc4Mjc2YmQ2ZTY1MDYyMDIxMDcyNDEzMjg0Nw==',
		   'PAY_URL':'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
		   'TOKEN_URL':'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'}