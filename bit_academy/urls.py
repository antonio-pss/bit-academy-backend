from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('bit_main.urls')),  # Incluindo as URLs do app 'bit_main'
]