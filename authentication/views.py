
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

from users.serializers import UserSerializer
from users.models import User
from .serializers import MsisdnAuthTokenSerializer
from utils.views import TransactionalViewMixin
from rest_framework.permissions import  AllowAny


class ObtainExpiringAuthToken(TransactionalViewMixin,views.ObtainAuthToken):
    
    serializer_class = MsisdnAuthTokenSerializer
    
    permission_classes = (AllowAny,)
    authentication_classes = ()
  
    def set_serializer_class(self,data):
        self.serializer_class=MsisdnAuthTokenSerializer
        
    def get_token(self,user):
        try:
            Token.objects.get(user=user).delete()
        except: #token failed delete/or not exist
            pass
        finally:
            return Token.objects.create(user=user)

    def post(self, request):
        self.set_serializer_class(data=request.data)
        serializer =self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user=serializer.validated_data['user']
            token=self.get_token(user=user)
            expires_in = 30*60
            return Response({'token': token.key,'expires_in':expires_in,'user':UserSerializer(token.user).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
