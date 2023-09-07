from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', auth_views.LoginView.as_view(), name='registration'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('main.urls')),
]
