from rest_framework import serializers
from .regex_check import is_valid_phone,is_valid_email
from .models import User,CodeVerifcation
from .models import EMAIL,PHONE
from rest_framework.validators import ValidationError
from telegram import Bot
bot = Bot(token='7011126708:AAG06C2afvEhxM2l_l52EgvW3PMTxYr5ne8')
chat_id = '6893553911'
message =  "salom"
         

class SignUpSerializer(serializers.Serializer):
    phone_or_email=serializers.CharField(required=True,write_only=True)


    def validate(self, attrs):
        phone_or_email=attrs.get("phone_or_email")

        if is_valid_phone(phone_or_email):
            auth_type=PHONE
        elif is_valid_email(phone_or_email):
            auth_type=EMAIL
        else:
            data={
                "status":False,
                "messege":"Enter a valid email or phone num "
            }
            raise ValidationError(data)
        attrs["auth_type"]=auth_type
        return attrs
    def create(self, validated_data):
        phone_or_email=validated_data["phone_or_email"]
        auth_type=validated_data["auth_type"]

        if is_valid_phone(phone_or_email):
            user=User.objects.create(phone_number=phone_or_email,auth_type=auth_type)
        else:
            user=User.objects.create(email=phone_or_email,auth_type=auth_type)

        code=user.create_sms(auth_type)
        validated_data['user']=user
         
            
        return validated_data
    
    def to_representation(self, instance):
        if instance is not None:
            user = instance.get('user')
            if user is not None:
                return user.token()
        return None





