from rest_framework import serializers
from django.conf import settings
from .models import User
import random
import string


class UserSerializer(serializers.ModelSerializer):
  
    permissions=serializers.ListField(read_only=True)


    class Meta:
        model = User
        exclude=('user_permissions','groups',)
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data): 
        created_by=validated_data.get('created_by')
        random_password=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        msisdn=validated_data.pop('msisdn')

        #create user
        password=validated_data.pop('password')

        user=User.objects.create_user(msisdn=msisdn,password=password,**validated_data)

        if created_by:
            password=random_password
            #send msisdn here . default gateway is gmail 
            msisdn_message="Welcome %s . Please use %s as your password. Make sure you change it later. "%(user.first_name,password)
            user.set_password(password)
        else:
            user.is_password_changed=True #creted by himself. doenot need to change password on login 
        
        user.save()
        return user



        
class UserChangePasswordSerializer(serializers.Serializer):
    #user=serializers.CharField(max_length=200,write_only=True)
    old_password=serializers.CharField(max_length=50,write_only=True)
    new_password=serializers.CharField(max_length=50,write_only=True)
    new_password_again=serializers.CharField(max_length=50,write_only=True)
    

    
   
class UserResetPasswordSerializer(serializers.Serializer):
    msisdn=serializers.CharField(max_length=50,write_only=True)
  

class UserVerifyEmailSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)

class UserVerifyPhoneSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)
    

class UserGroupManageUserSerializer(serializers.Serializer):
    group=serializers.IntegerField()
    action=serializers.IntegerField()
    user=serializers.CharField(max_length=300)
