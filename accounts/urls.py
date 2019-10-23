from django.urls import path
from accounts import views 
app_name="accounts"

urlpatterns = [
    path('login/',views.loginview,name="login"),
    path('logout/',views.logoutview,name="logout"),
    path('register',views.register,name="register"),
]
