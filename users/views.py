from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer
from .models import CodeVerifcation
from datetime import datetime,timedelta
from rest_framework.validators import ValidationError
from .regex_check import is_valid_phone,is_valid_email
from django.contrib.auth import authenticate


class SignUpView(APIView):
    def post(self,request):
        serialazer=SignUpSerializer(data=request.data)
        serialazer.is_valid(raise_exception=True)
        serialazer.save()

        return Response(serialazer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if not user:
            raise ValidationError("Noto'g'ri nom yoki parol")
        
         
        if user.is_authenticated:
            data = {
                "auth_status": user.auth_status,
                "access_token": user.token()['access'],
                "refresh_token": user.token()['refresh_token'],
            }
            return Response(data)
         
        raise ValidationError("Foydalanuvchi ro'yxatdan o'tmagan")



class CodeVerifcationView(APIView):
    def post(self,request):
        codes=CodeVerifcation.objects.all()
        user = self.request.user
        code = self.request.data.get('code')

        self.check_code(user, code)
        data = {
            "status": True,
            "auth_status": user.auth_status,
            "access_token": user.token()['access'],
            "refresh_token": user.token()['refresh_token'],
        }
        return Response(data)

    @staticmethod
    def check_code(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Xatolik qaytadan urining"
            }
            raise ValidationError(data)
        verifies.update(is_confirmed=True)
         
        
          
        