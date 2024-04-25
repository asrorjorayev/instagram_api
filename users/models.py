from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime,timedelta
import uuid
import random
NEW,CODE_VERIFY,DONE,PHOTO_DONE=(' new','code_verify','done','photo_done')
EMAIL,PHONE=('email','phone')

class User(AbstractUser):
    AUTH_STEP=(
        (NEW,NEW),
        (CODE_VERIFY,CODE_VERIFY),
        (DONE,DONE),
        (PHOTO_DONE,PHOTO_DONE)
    )

    AUTH_TYPE=(
        (EMAIL,EMAIL),
        (PHONE,PHONE)
    )
    phone_number=models.CharField(max_length=13,unique=True,db_index=True)
    image=models.ImageField(upload_to='image/',null=True)
    auth_step=models.CharField(choices=AUTH_STEP,max_length=50,default=NEW)
    auth_type=models.CharField(choices=AUTH_TYPE,max_length=30)
    

    def clean_username(self):
        if not self.username:
            temp_username=f"instagram-{str(uuid.uuid4()).split('-')[-1]}"
             
            self.username=temp_username
    def clean_password(self):
        if not self.password :
            self.password=f"instagram-{str(uuid.uuid4()).split('-')[-1]}"
    
    def hash_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
    
    def clean_all(self):
        self.clean_username()
        self.clean_password()
        self.has_usable_password()

    def save(self,*args,**kwargs):
        self.clean_all()

        super(  User,self).save(*args,**kwargs)
    def token(self):
        refrash=RefreshToken.for_user(self)
        return {
            "refrash":str(refrash),
            "acces":str(refrash.access_token)
        }
    def create_sms(self,auth_type):
        code= "".join(str(random.randint(0,9)) for _ in range(5))
        CodeVerifcation.objects.create(
            code=code,
            auth_type=auth_type
        )

        
class CodeVerifcation(models.Model):
    AUTH_TYPE=(
        (EMAIL,EMAIL),
        (PHONE,PHONE)
    )

    code=models.CharField(max_length=5)
    auth_type=models.CharField(max_length=50,choices=AUTH_TYPE)
    expire_time=models.DateTimeField()
    is_varification=models.BooleanField(default=False)
    user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='verefication')

    def save(self,*args,**kwargs):
        if self.auth_type==EMAIL:
            self.expire_time=datetime.now()+timedelta(minutes=2)
        elif self.auth_type==PHONE:
            self.expire_time=datetime.now()+timedelta(minutes=2)
        super(CodeVerifcation,self).save(*args,**kwargs)




        
        
