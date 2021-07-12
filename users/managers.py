
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, msisdn, password, **extra_fields):
        #do validations
        if not msisdn:
            raise ValueError('The given msisdn must be set')
        msisdn = self.normalize_msisdn(msisdn)
        user = self.model(msisdn=msisdn, **extra_fields)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_user(self, msisdn,password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(msisdn,password,**extra_fields)
        
    
   
    

    def create_superuser(self, msisdn,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(msisdn, password, **extra_fields)
    
    def normalize_msisdn(self,msisdn):
        return msisdn.strip('+')
        
        

