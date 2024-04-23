from django.contrib import admin
from .models import User,CodeVerifcation

admin.site.register([User,CodeVerifcation])
# Register your models here.
