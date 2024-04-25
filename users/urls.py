from django.urls import path
from .views import SignUpView,CodeVerifcation

app_name='users'
urlpatterns=[
    path('signup/',SignUpView.as_view(),name='signup'),
    # path('veroficaty/',CodeVerifcation.as_view(),name='verefication'),
]