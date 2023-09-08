from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('registration/', auth_views.LoginView.as_view(), name='registration'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('', include('main.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
