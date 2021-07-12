
from users.models import User

class CustomBackend(object):
    """authenticate when given msisdn, password """
    
  
    def get_by_msisdn(self,msisdn,password):
        try:
            user = User.objects.get(msisdn=msisdn)
            if password:
                if user.check_password(password):
                    return user
            else:
                return user
        except User.DoesNotExist:
            pass


    def authenticate(self, msisdn=None, password=None, **kwargs):
        if not msisdn:
            return None
        return self.get_by_msisdn(msisdn,password)

            
        
        
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
        
        
        